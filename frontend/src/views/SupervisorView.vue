<template>
    <v-card title="Approbation" flat>
        <!-- <v-container>            -->
        <template v-slot:text>
            <v-text-field v-model="search" label="Search" prepend-inner-icon="mdi-magnify" variant="outlined"
                hide-details single-line></v-text-field>
        </template>
        <v-data-table v-model="selectedTimesheets" :headers="headers" :items="fetchedTimesheets" :search="search"
            item-value="employee" show-select>
            <template v-slot:item.exclusive="{ item }">
                <v-checkbox v-model="item.exclusive" readonly></v-checkbox>
            </template>
        </v-data-table>
        <v-btn color="primary" @click="approveSelectedTimesheets">Approve Selected</v-btn>
        <!-- </v-container> -->

    </v-card>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const search = ref(''); //
const selectedTimesheets = ref([]);
const fetchedTimesheets = ref([]);
const approvedTimesheets = ref([]);
const headers = [
    { title: 'Employee', key: 'employee' },
    { title: 'Timesheet ID', key: 'timesheet_id' },
    { title: 'Date', key: 'date' },
    { title: 'Month', key: 'month' },
    { title: 'Project', key: 'project' },
    { title: 'Worked Days', key: 'worked' },
    { title: 'Actions', key: 'actions', sortable: false },
];

onMounted(async () => {
    await fetchTimesheets();
});

async function fetchTimesheets() {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket("ws://localhost:8765");
        const date = new Date(); // Get the current date
        const month = date.toLocaleString('default', { month: 'long' });

        ws.onopen = () => {
            ws.send(JSON.stringify({ action: "fetch_timesheet", month }));
        };

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);
            if (response.success && Array.isArray(response.timesheets)) {
                // Transform the data into the required format
                fetchedTimesheets.value = response.timesheets.map(timesheet => ({
                    timesheet_id: timesheet[0],
                    user_id: timesheet[1],
                    employee: timesheet[6] + ' ' + timesheet[7],
                    date: timesheet[2],
                    month: timesheet[3],
                    project: timesheet[4],
                    worked: timesheet[5]
                }));
            } else {
                console.error("Unexpected response format:", response);
            }
            resolve(response);
            ws.close();
        };

        ws.onerror = (error) => {
            console.error("WebSocket error:", error);
            alert("Failed to connect to the WebSocket server.");
            reject(error);
        };

        ws.onclose = () => {
            console.log("WebSocket connection closed.");
        };
    });
}

async function approveSelectedTimesheets() {
    const user = JSON.parse(localStorage.getItem('user'));
    if (!user) {
        alert("User not logged in");
        return;
    }

    // console.log(fetchedTimesheets);
    for (const selectedTimesheet of selectedTimesheets.value) {
        const result = fetchedTimesheets.value.find(({ employee }) => employee === selectedTimesheet);
        approvedTimesheets.value.push(result)
    }
    // console.log(approvedTimesheets)
    const super_id = user.user_id
    for (const timesheet of approvedTimesheets.value) {
        // console.log(timesheet);
        const response = await approveTimesheet(timesheet.timesheet_id, super_id, true, new Date().toISOString().substring(0, 10));
        if (!response.success) {
            alert("Failed to approve timesheet");
            return;
        }
    }

    alert("Timesheets approved successfully");
    selectedTimesheets.value = [];
    approvedTimesheets.value = [];
}

async function approveTimesheet(timesheet_id, supervisor_id, approved, approval_date) {
    return new Promise((resolve, reject) => {
        const ws = new WebSocket("ws://localhost:8765");

        ws.onopen = () => {
            ws.send(JSON.stringify({ action: "approve_timesheet", timesheet_id, supervisor_id, approved, approval_date }));
        };

        ws.onmessage = (event) => {
            const response = JSON.parse(event.data);
            resolve(response);
            ws.close();
        };

        ws.onerror = (error) => {
            reject(error);
        };
    });
}
</script>