<template>
  <div class="user-data">
    <h2>User Data</h2>
    <v-form @submit.prevent="updateUser">
      <v-container>
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.firstName" color="primary" :rules="[(v) => !!v || 'Item is required']"
              hide-details="auto" label="First name" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.lastName" color="primary" :rules="[(v) => !!v || 'Item is required']"
              hide-details="auto" label="Last name" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.email" color="primary" :rules="[(v) => !!v || 'Item is required']"
              hide-details="auto" label="Email" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.phone" color="primary" :rules="[(v) => !!v || 'Item is required']"
              hide-details="auto" label="Tel." variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select :items="['Contract', 'Supervisor', 'Employee']" v-model="user.role" :rules="rules"
              hide-details="auto" color="primary" label="Role" variant="underlined"></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.contractNumber" color="primary" :rules="rules" hide-details="auto"
              label="Contract number" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.company" color="primary" label="Company" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.taxNumber" color="primary" label="Tax number"
              variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.client" color="primary" label="Client" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select v-model="user.project" :items="projects" item-text="project_name" item-value="project_id"
              label="Project" required></v-select>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.city" color="primary" label="City" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.dateStart" color="primary" label="Start Date"
              variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.dateEnd" color="primary" label="End Date" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="user.rate" color="primary" label="Rate" variant="underlined"></v-text-field>
          </v-col>
          <v-col cols="12" md="12">
            <v-btn color="primary" type="submit">Update</v-btn>
          </v-col>
        </v-row>
      </v-container>
    </v-form>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';

const user = ref({
  firstName: "",
  lastName: "",
  email: "",
  phone: "",
  role: "",
  contractNumber: "",
  company: "",
  taxNumber: "",
  client: "",
  project: "",
  city: "",
  dateStart: "",
  dateEnd: "",
  rate: "",
});

const projects = ref([]);

const rules = [
  (value) => !!value || "Required.",
  (value) => (value && value.length >= 3) || "Min 3 characters",
];

const updateUser = async () => {
  const userData = { ...user.value, user_id: JSON.parse(localStorage.getItem('user')).id };
  const response = await updateUserData(userData);
  if (response.success) {
    alert("User data updated successfully");
  } else {
    alert("Failed to update user data");
  }
};

async function updateUserData(user_data) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
      ws.send(JSON.stringify({ action: "update_user_data", user_data }));
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

async function fetchProjects() {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket("ws://localhost:8765");

    ws.onopen = () => {
      ws.send(JSON.stringify({ action: "get_projects" }));
    };

    ws.onmessage = (event) => {
      const response = JSON.parse(event.data);
      if (response.success) {
        projects.value = response.projects; // Update the projects ref with the fetched projects
      }
      resolve(response); // Resolve the promise with the response
      ws.close(); // Close the WebSocket connection
    };

    ws.onerror = (error) => {
      reject(error); // Reject the promise if there's an error
    };
  });
}

onMounted(async () => {
  await fetchProjects(); // Fetch projects when the component is mounted
});
</script>

<style scoped>
.user-data {
  padding: 1rem;
  border: 1px solid #ccc;
  border-radius: 8px;
  max-width: 800px;
  margin: 1rem auto;
}

.user-data h2 {
  margin-bottom: 1rem;
}

.v-container {
  color: #ccc;
}

.v-sheet {
  border-color: rgb(0, 0, 0) !important;
}
</style>
