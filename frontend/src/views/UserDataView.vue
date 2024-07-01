<script setup>
import { ref } from "vue";
// import { shallowRef } from 'vue'
// import { useDate } from 'vuetify'
// const date = shallowRef()
const user = ref({
  firstName: "",
  lastName: "",
  phone: "",
  email: "",
  role: "",
  contractNumber: "",
  company: "",
  taxNumber: "",
  client: "",
  city: "",
  dateStart: "",
  dateEnd: "",
  rate: "",
});

const updateUser = () => {
  console.log("User data updated:", user.value);
};
data: () => ({
  rules: [
    (value) => !!value || "Required.",
    (value) => (value && value.length >= 3) || "Min 3 characters",
  ],
  emailRules: [
    (value) => {
      if (value) return true;

      return "E-mail is requred.";
    },
    (value) => {
      if (/.+@.+\..+/.test(value)) return true;

      return "E-mail must be valid.";
    },
  ],
  nameRules: [
    (value) => {
      if (value) return true;

      return "Name is required.";
    },
    (value) => {
      if (value?.length <= 10) return true;

      return "Name must be less than 10 characters.";
    },
  ],
  otherRules: [
    (value) => !!value || "Required.",
    (value) => (value || "").length <= 20 || "Max 20 characters",
    (value) => {
      const pattern =
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
      return pattern.test(value) || "Invalid e-mail.";
    },
  ],
});
</script>

<template>
  <div class="user-data">
    <!-- <h2>User Registration</h2> -->
    <!-- <form @submit.prevent="updateUser"> -->
    <v-sheet class="d-flex" height="600" color="transparent">
      <v-form v-model="valid">
        <!-- <v-form ref="form"> -->
        <!-- <v-card
      class="mx-auto"
      max-width="344"
      title="User Registration"
    > -->
        <v-container>
          <v-row>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.firstName"
                hide-details="auto"
                color="primary"
                label="First name"
                :rules="[(v) => !!v || 'Item is required']"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.lastName"
                color="primary"
                :rules="[(v) => !!v || 'Item is required']"
                hide-details="auto"
                label="Last name"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.email"
                color="primary"
                :rules="[(v) => !!v || 'Item is required']"
                hide-details="auto"
                label="Email"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.phone"
                color="primary"
                :rules="[(v) => !!v || 'Item is required']"
                hide-details="auto"
                label="Tel."
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-select
                :items="['Contract', 'Supervisor', 'Employee']"
                v-model="user.role"
                :rules="rules"
                hide-details="auto"
                color="primary"
                label="Role"
                variant="underlined"
              ></v-select>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.contractNumber"
                color="primary"
                :rules="rules"
                hide-details="auto"
                label="Contract number"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.company"
                color="primary"
                label="Company"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.taxNumber"
                color="primary"
                label="Tax number"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.client"
                color="primary"
                label="Client"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.city"
                color="primary"
                label="City"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.dateStart"
                :rules="rules"
                hide-details="auto"
                color="primary"
                label="Date Start"
                model-value="01/01/2001"
                suffix=""
                type="date"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.dateEnd"
                :rules="rules"
                hide-details="auto"
                color="primary"
                label="Date End"
                model-value="01/01/2001"
                suffix=""
                type="date"
                variant="underlined"
              ></v-text-field>
            </v-col>
            <v-col cols="12" md="6">
              <v-text-field
                v-model="user.rate"
                color="primary"
                label="Rate"
                variant="underlined"
                suffix="Eur."
              ></v-text-field>
            </v-col>
          </v-row>
        </v-container>
        <v-btn type="submit" color="primary">Save</v-btn>
        <v-divider></v-divider>
        <!-- <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn color="success">
          Complete Registration
          <v-icon icon="mdi-chevron-right" end></v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>     -->
      </v-form>
      <sheet-footer> #1: (3r x 2c) </sheet-footer>
    </v-sheet>
  </div>
</template>

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
</style>
