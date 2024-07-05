<!-- <template>
    <v-container>
        <v-data-table v-model="selectedTimesheets" :headers="headers" :items="timesheets" item-value="employee"
            show-select>
        </v-data-table>,
        <v-btn color="primary" @click="approveSelectedTimesheets">Approve Selected</v-btn>
    </v-container>
</template> -->

<template>
    <v-container>
        <!-- <v-data-table :items="consoles"> -->
        <v-data-table v-model="selectedTimesheets" :headers="headers" :items="fetchedTimesheets" item-value="employee"
            show-select>
            <template v-slot:item.exclusive="{ item }">
                <v-checkbox v-model="item.exclusive" readonly></v-checkbox>
            </template>
        </v-data-table>
        <v-btn color="primary" @click="approveSelectedTimesheets">Approve Selected</v-btn>
    </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const selectedTimesheets = ref([]);
const timesheets = ref([]);
const selectAll = ref(false);
const headers = [
    { title: 'Employee', key: 'employee' },
    { title: 'Date', key: 'date' },
    // { title: 'Hours', key: 'hours' },
    { title: 'Days Worked', key: 'daysWorked' },
    { title: 'Actions', key: 'actions', sortable: false },
];
const fetchedTimesheets = [
    { id: 1, employee: 'John Doe', date: '2023-10-01', daysWorked: 19, selected: false },
    { id: 2, employee: 'Jane Smith', date: '2023-10-02', daysWorked: 19, selected: false },
    { id: 3, employee: 'John Doe1', date: '2023-10-01', daysWorked: 19, selected: false },
    { id: 4, employee: 'Jane Smith1', date: '2023-10-02', daysWorked: 19, selected: false },
    // Add more timesheets here
];
onMounted(async () => {
    // await fetchTimesheets();
});

async function fetchTimesheets() {
    // Fetch the timesheets data for the current month
    // This is a placeholder, replace with your actual data fetching logic
    // const fetchedTimesheets = [
    //     { id: 1, employee: 'John Doe', date: '2023-10-01', hours: 8, daysWorked: 19, selected: false },
    //     { id: 2, employee: 'Jane Smith', date: '2023-10-02', hours: 7.5, daysWorked: 19, selected: false },
    //     // Add more timesheets here
    // ];

    // Calculate the number of days worked for each timesheet entry
    timesheets.value = fetchedTimesheets.map(timesheet => {
        // const daysWorked = calculateDaysWorked(timesheet.date);
        const daysWorked = timesheet.daysWorked;
        return { ...timesheet, daysWorked };
    });
}

function calculateDaysWorked(date) {
    // Implement your logic to calculate the number of days worked
    // This is a placeholder implementation
    const startDate = new Date(date);
    const endDate = new Date();
    const timeDiff = Math.abs(endDate - startDate);
    const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
    return daysDiff;
}

function toggleSelectAll() {
    timesheets.value.forEach(timesheet => {
        timesheet.selected = selectAll.value;
    });
}

function handleSelectAllClick() {
    console.log('Select All header clicked');
}

function approveSelectedTimesheets() {
    console.log(selectedTimesheets)
    // const selectedTimesheets = timesheets.value.filter(timesheet => timesheet.selected);
    // console.log('Approving selected timesheets:', selectedTimesheets);
    // Add your approval logic here
}
</script>
