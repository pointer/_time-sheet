<!-- <template>
  <v-form @submit.prevent="login">
    <v-text-field v-model="username" label="Username" required></v-text-field>
    <v-text-field v-model="password" label="Password" type="password" required></v-text-field>
    <v-btn type="submit" color="primary">Login</v-btn>
  </v-form>
</template> -->

<template>
  <v-sheet class="bg-deep-purple pa-12" rounded>
    <v-card class="mx-auto px-6 py-8" max-width="344">
      <v-form v-model="form" @submit.prevent="login">
        <v-text-field v-model="username" :readonly="loading" :rules="[required]" class="mb-2" label="Username"
          clearable></v-text-field>

        <v-text-field v-model="password" :readonly="loading" :rules="[required]" label="Password"
          placeholder="Enter your password" clearable></v-text-field>

        <br>

        <v-btn :disabled="!form" :loading="loading" color="success" size="large" type="submit" variant="elevated" block>
          Sign In
        </v-btn>
      </v-form>
    </v-card>
  </v-sheet>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const username = ref('');
const password = ref('');
const router = useRouter();

async function login() {
  // Replace with your actual login API call
  const response = await fakeLoginApi(username.value, password.value);
  if (response.success) {
    localStorage.setItem('user', JSON.stringify(response.user));
    if (response.user.role === 'supervisor') {
      router.push('/supervisor');
    } else if (response.user.role === 'employee') {
      router.push('/time-sheet');
    }
    else if (response.user.role === 'admin') {
      router.push('/');
    }
  } else {
    alert('Login failed');
  }
}

async function fakeLoginApi(username, password) {
  // Simulate an API call
  return new Promise((resolve) => {
    setTimeout(() => {
      if (username === 'supervisor' && password === 'password') {
        resolve({ success: true, user: { role: 'supervisor' } });
      } else if (username === 'employee' && password === 'password') {
        resolve({ success: true, user: { role: 'employee' } });
      } else {
        resolve({ success: false });
      }
    }, 1000);
  });
}
</script>
