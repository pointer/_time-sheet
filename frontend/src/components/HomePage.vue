<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <h1 class="text-h3 font-weight-bold mb-4">Welcome to TimeSheet App</h1>
        <p class="text-subtitle-1">Manage your time efficiently with our easy-to-use platform</p>
      </v-col>
    </v-row>

    <v-row class="mt-8">
      <v-col v-for="(feature, index) in features" :key="index" cols="12" md="4">
        <v-card class="mx-auto" max-width="400">
          <v-card-text class="text-center">
            <v-icon size="48" color="primary" class="mb-4">{{ feature.icon }}</v-icon>
            <h2 class="text-h5 font-weight-bold mb-2">{{ feature.title }}</h2>
            <p>{{ feature.description }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn :to="feature.link" color="primary" text>Learn More</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="mt-8">
      <v-col cols="12">
        <v-btn color="primary" large :to="'/user-data'">Get Started</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'

const features = ref([
  {
    icon: 'mdi-clock-outline',
    title: 'Time Tracking',
    description: 'Easy and accurate time tracking for all your projects.',
    link: '/time-sheet'
  },
  {
    icon: 'mdi-account-group',
    title: 'User Management',
    description: 'Efficiently manage users and their roles.',
    link: '/user-data'
  },
  {
    icon: 'mdi-chart-bar',
    title: 'Reports',
    description: 'Generate insightful reports for better decision making.',
    link: '/admin'
  }
])
</script>

<style scoped>

.read-the-docs {
  color: #888;
}
</style>
