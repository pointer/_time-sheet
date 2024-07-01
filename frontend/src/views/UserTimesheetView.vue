<template>
  <v-container>
    <h1 class="text-h4 mb-5">Time Sheet</h1>

    <!-- Time Entry Form -->
    <v-form @submit.prevent="addTimeEntry" ref="form">
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="newEntry.date"
            label="Date"
            type="date"
            required
          ></v-text-field>
        </v-col>
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
        <v-col cols="12" md="3">
          <v-btn color="primary" type="submit" :disabled="!formIsValid">
            Add Entry
          </v-btn>
        </v-col>
      </v-row>
    </v-form>

    <!-- Time Entries Table -->
    <v-data-table
      :headers="headers"
      :items="timeEntries"
      class="elevation-1 mt-5"
    >
      <template v-slot:item.actions="{ item }">
        <v-icon small @click="deleteEntry(item)">
          mdi-delete
        </v-icon>
      </template>
    </v-data-table>
  </v-container>
</template>

<script setup>
import { ref, computed } from 'vue'

const newEntry = ref({
  date: '',
  project: '',
  hours: null
})

const timeEntries = ref([])

const headers = [
  { text: 'Date', value: 'date' },
  { text: 'Project', value: 'project' },
  { text: 'Hours', value: 'hours' },
  { text: 'Actions', value: 'actions', sortable: false }
]

const form = ref(null)

const formIsValid = computed(() => {
  return newEntry.value.date && newEntry.value.project && newEntry.value.hours > 0
})

function addTimeEntry() {
  if (formIsValid.value) {
    timeEntries.value.push({ ...newEntry.value })
    form.value.reset()
    newEntry.value = { date: '', project: '', hours: null }
  }
}

function deleteEntry(item) {
  const index = timeEntries.value.indexOf(item)
  timeEntries.value.splice(index, 1)
}
</script>