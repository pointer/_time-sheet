<template>
  <v-main>
    <v-app-bar app>
      <v-toolbar-title>Time Sheet</v-toolbar-title>
      <v-spacer></v-spacer>
      <LogoutButton />
    </v-app-bar>
    <h1 class="text-h4 mb-5">Time Sheet</h1>

    <v-container>
      <v-row>
        <!-- Date Picker -->
        <v-col cols="12" md="4">
          <v-date-picker show-adjacent-months multiple :dark="theme.global.current.value.dark" color="primary"
            v-model="newEntry.dates" scrollable :allowed-dates="allowedDates"></v-date-picker>
        </v-col>

        <!-- Time Entries Table -->
        <v-col cols="12" md="8">
          <v-data-table :headers="headers" :items="timeEntries" class="elevation-1 mt-5">
            <template #item.actions="{ item }">
              <v-icon small @click="deleteEntry(item)">mdi-delete</v-icon>
            </template>
          </v-data-table>

          <!-- Buttons -->
          <v-row justify="end" class="mt-4">
            <v-col cols="auto">
              <v-btn height="72" min-width="164" color="primary" type="submit" @click="addTimeEntry"
                :disabled="!formIsValid">
                Add Entry
              </v-btn>
            </v-col>
            <v-col cols="auto">
              <v-btn height="72" min-width="164" @click="saveTimesheet">
                Save
              </v-btn>
            </v-col>
          </v-row>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script setup>
import { ref, computed, onMounted } from "vue";
import { useTheme } from "vuetify";
import { isWeekend, isHoliday } from "@/utils/utils"; // Assume you have a utility to check holidays
// import LogoutButton from "@/components/LogoutButton.vue";

const theme = useTheme();
const newEntry = ref({
  dates: [],
});

// const timeEntries = ref([
//   { date: "2023-10-01", project: "Project A", worked: 20 },
//   { date: "2023-10-02", project: "Project B", worked: 22 },
// ]);

const timeEntries = ref([]);

const projects = ref([]);

const headers = [
  { title: "Dates", key: "date" },
  { title: "Worked Days", key: "worked" },
  { title: "Biz days", key: "working_days", sortable: false },
  { title: "Actions", key: "actions", sortable: false },

];

const form = ref(null);
const dateMenu = ref(false);

const formIsValid = computed(() => {
  return newEntry.value.dates.length > 0;
});

function formatDate(date) {
  if (!date) return null;
  const [year, month, day] = date.split('-');
  return `${year}-${month}-${day}`;
}

function formatDateForDisplay(date) {
  if (!date) return null;
  const [year, month, day] = date.split('-');
  return `${day}/${month}/${year}`;
}

function addTimeEntry() {
  if (formIsValid.value) {
    let count = 0;
    let dateFormatted = new Date().toLocaleDateString();

    newEntry.value.dates.forEach((date) => {
      count++;
    });

    timeEntries.value.push({
      date: dateFormatted,
      worked: count,
      working_days: working_days
    });

    if (form.value) {
      form.value.reset();
    }
    newEntry.value = { dates: [] };
  }
}

function deleteEntry(item) {
  const index = timeEntries.value.indexOf(item);
  timeEntries.value.splice(index, 1);
}

function onDateChange(dates) {
  newEntry.value.dates = dates;
}

function allowedDates(date) {
  return !isWeekend(date) && !isHoliday(date);
}


async function saveTimesheet() {
  const user = JSON.parse(localStorage.getItem('user'));
  if (!user) {
    alert("User not logged in");
    return;
  }
  const date = new Date(); // Get the current date
  const month = date.toLocaleString('default', { month: 'long' }); //
  for (const entry of timeEntries.value) {
    const response = await submitTimesheet(user.user_id, entry.date, entry.worked, month);
    if (!response.success) {
      alert("Failed to save timesheet");
      return;
    }
  }

  alert("Timesheet saved successfully");
  timeEntries.value = [];
}

async function submitTimesheet(user_id, date, worked, month) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
      ws.send(JSON.stringify({ action: "submit_timesheet", user_id, date, worked, month }));
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
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

async function fetchProjects() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
      ws.send(JSON.stringify({ action: "get_projects" }));
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.success) {
        projects.value = response.projects;
      }
      resolve(response);
      ws.close();
    };

    ws.onerror = (error) => {
      reject(error);
    };
  });
}

onMounted(async () => {
  await fetchProjects();
});
</script>