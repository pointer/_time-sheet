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

import { ref, computed, onMounted } from "vue";
import { useTheme } from "vuetify";
import { isWeekend, isHoliday } from "@/utils/utils"; // Assume you have a utility to check holidays
import { useRouter } from "vue-router";
const theme = useTheme();
import { useApprobationStore } from "@/store";
const router = useRouter();
const approbationStore = useApprobationStore();
import { useField, useForm, ErrorMessage } from "vee-validate";
import { NavigationFailureType, isNavigationFailure } from "vue-router";
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
    try {
        const date = new Date();
        const month = date.toLocaleString('default', { month: 'long' });
        const token = localStorage.getItem('token');
        if (!token) {
            throw new Error('No authentication token found');
        }
        const response = await approbationStore.getTimesheetsByMonth(month, token);
        console.log('Timesheets response:', response);
        fetchedTimesheets.value = response;
    } catch (error) {
        console.error('Error fetching timesheets:', error);
        // Handle the error, e.g., redirect to login page or show an error message
    }
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