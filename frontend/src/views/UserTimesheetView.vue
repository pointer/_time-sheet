<template>
  <!-- <v-container> -->
  <v-main>
    <h1 class="text-h4 mb-5">Time Sheet</h1>

    <!-- Time Entry Form -->
    <v-form @submit.prevent="addTimeEntry" dark ref="form">
      <v-container>
        <v-row class="mb-6" no-gutters>
          <v-col cols="12" md="4">
            <v-date-picker show-adjacent-months multiple :dark="theme.global.current.value.dark" color="primary"
              v-model="newEntry.dates" scrollable></v-date-picker>
          </v-col>
          <v-col cols="12" md="8">
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="newEntry.project" label="Project" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model.number="newEntry.hours" label="Hours" type="number" min="0" step="0.5" required
                  width=140 maxlength=4></v-text-field>
              </v-col>
              <v-row justify="right">
                <v-col cols="auto">
                  <v-btn height="72" min-width="164" color="primary" type="submit" :disabled="!formIsValid">
                    Add Entry
                  </v-btn>
                </v-col>
              </v-row>
            </v-row>
          </v-col>
        </v-row>
      </v-container>
    </v-form>

    <!-- Time Entries Table -->
    <v-data-table :headers="headers" :items="timeEntries" class="elevation-1 mt-5">
      <template #item.actions="{ item }">
        <v-icon small @click="deleteEntry(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>
    <v-container>
      <v-row justify="center">
        <v-col cols="auto">
          <v-btn height="72" min-width="164" @click="saveTimesheet">
            Save
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <!-- </template> -->
  </v-main>
  <!-- </v-container> -->
</template>

<script setup>
import { ref, computed } from "vue";
import { useTheme } from "vuetify";

const theme = useTheme();
const newEntry = ref({
  dates: [],
  project: "",
  hours: null,
});

const timeEntries = ref([]);

const headers = [
  { title: "Dates", key: "date" },
  { title: "Project", key: "project" },
  { title: "Hours", key: "hours" },
  { title: "Actions", key: "actions", sortable: false },
];

// console.log("Headers:", headers); // Verify headers
// console.log("Time Entries:", timeEntries.value); // Verify time entries

const form = ref(null);
const dateMenu = ref(false);

const formIsValid = computed(() => {
  return (
    newEntry.value.dates.length > 0 &&
    newEntry.value.project &&
    newEntry.value.hours > 0
  );
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
    newEntry.value.dates.forEach((date) => {
      const dateString = date.toISOString().substring(0, 10);
      const dateFormatted = formatDateForDisplay(dateString);
      timeEntries.value.push({
        date: dateFormatted,
        project: newEntry.value.project,
        hours: newEntry.value.hours,
      });
    });
    form.value.reset();
    newEntry.value = { dates: [], project: "", hours: null };
  }
}

function deleteEntry(item) {
  const index = timeEntries.value.indexOf(item);
  timeEntries.value.splice(index, 1);
}

function onDateChange(dates) {
  newEntry.value.dates = dates;
}

function saveTimesheet() {
  // Implement the logic to save the timesheet
  console.log("Saving timesheet:", timeEntries.value);
  // You can send the `timeEntries` data to your backend here
}
</script>
