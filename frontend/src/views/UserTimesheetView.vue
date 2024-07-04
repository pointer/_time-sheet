<template>
  <v-container>
    <h1 class="text-h4 mb-5">Time Sheet</h1>

    <!-- Time Entry Form -->
    <v-form @submit.prevent="addTimeEntry" dark ref="form">
      <v-container>
        <!-- <v-row justify="space-around"> -->
          <v-date-picker
            show-adjacent-months
            multiple
            :dark="$vuetify.theme.defaultTheme"
            color="primary"
          ></v-date-picker>
        <!-- </v-row> -->
        <!-- </v-container> -->
        <!-- <v-row > -->
        <v-col cols="12" md="3">
          <v-text-field
            v-model="newEntry.project"
            label="Project"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model.number="newEntry.hours"
            label="Hours"
            type="number"
            min="0"
            step="0.5"
            required
          ></v-text-field>
        </v-col>
        <v-col cols="6" offset="4">
          <v-btn
            size="x-large"
            color="primary"
            type="submit"
            :disabled="!formIsValid"
          >
            Add Entry
          </v-btn>
        </v-col>
        <v-col cols="6" offset="3">
          <v-sheet class="pa-2 ma-2"> .v-col-6 .offset-3 </v-sheet>
        </v-col>
        <!-- </v-row> -->
      </v-container>
    </v-form>

    <!-- Time Entries Table -->
    <v-data-table
      :headers="headers"
      :items="timeEntries"
      class="elevation-1 mt-5"
    >
      <template #item.actions="{ item }">
        <v-icon small @click="deleteEntry(item)">mdi-delete</v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed } from "vue";
import vuetify from "../plugins/vuetify";
import { useTheme } from "vuetify"; // Add this line

const theme = useTheme(); // Add this line
const newEntry = ref({
  dates: [],
  project: "",
  hours: null,
});

const timeEntries = ref([]);

const headers = [
  { text: "Dates", value: "dates" },
  { text: "Project", value: "project" },
  { text: "Hours", value: "hours" },
  { text: "Actions", value: "actions", sortable: false },
];

const form = ref(null);
const dateMenu = ref(false);

const formIsValid = computed(() => {
  return (
    newEntry.value.dates.length > 0 &&
    newEntry.value.project &&
    newEntry.value.hours > 0
  );
});

function addTimeEntry() {
  if (formIsValid.value) {
    newEntry.value.dates.forEach((date) => {
      timeEntries.value.push({
        date,
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
</script>
