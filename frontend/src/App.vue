<script setup>
import {
  ref,
  onMounted,
  onBeforeUnmount,
  onUnmounted,
  reactive,
  computed,
  watch,
} from "vue";
import { RouterLink, RouterView } from "vue-router";

const drawer = ref(false);
const group = ref(null);
const windowWidth = ref(window.innerWidth);
const showOverlay = computed(() => drawer.value && !permanent.value);

const closeDrawer = () => {
  drawer.value = false;
};
const items = ref([
  { title: "Home", value: "home", route: "/" },
  { title: "User Registrar", value: "user-data", route: "/user-data" },
  { title: "Time Sheet", value: "bar", route: "/time-sheet" },
  { title: "Validation", value: "fizz", route: "/validation" },
  { title: "Admin", value: "buzz", route: "/admin" },
]);
const permanent = computed(() => {
  return windowWidth.value >= 1264; // Equivalent to Vuetify's 'lg' breakpoint
});

const handleResize = () => {
  windowWidth.value = window.innerWidth;
};

const handleOutsideClick = (event) => {
  if (drawer.value && !permanent.value) {
    const navDrawer = document.querySelector(".v-navigation-drawer");
    const appBar = document.querySelector(".v-app-bar");
    if (
      navDrawer &&
      !navDrawer.contains(event.target) &&
      !appBar.contains(event.target)
    ) {
      drawer.value = false;
    }
  }
};

onMounted(() => {
  window.addEventListener("resize", handleResize);
  document.addEventListener("click", handleOutsideClick);
});

onBeforeUnmount(() => {
  window.removeEventListener("resize", handleResize);
  document.removeEventListener("click", handleOutsideClick);
});
watch(group, () => {
  drawer.value = false;
});
</script>
<template>
  <v-app>
    <!-- <v-app-bar color="primary" dark app elevation="4" :height="64">
      <v-app-bar-nav-icon @click.stop="toggleDrawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Time Sheet</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon>mdi-magnify</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-apps</v-icon>
      </v-btn>
      <v-btn icon>
        <v-icon>mdi-dots-vertical</v-icon>
      </v-btn>
    </v-app-bar> -->
    <v-app-bar :elevation="2">
      <template v-slot:prepend>
        <v-app-bar-nav-icon></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>Application Bar</v-app-bar-title>
    </v-app-bar>
    <v-card>
      <v-layout>
        <v-navigation-drawer expand-on-hover rail>
          <v-list>
            <router-link
              v-for="item in items"
              :key="item.value"
              :to="item.route"
              custom
              v-slot="{ navigate, isActive }"
            >
              <v-list-item :active="isActive" @click="navigate">
                <v-list-item-title>{{ item.title }}</v-list-item-title>
              </v-list-item>
            </router-link>
          </v-list>
          <template v-slot:append>
            <div class="pa-2">
              <v-btn block @click="drawer = !drawer"> Logout </v-btn>
            </div>
          </template>
        </v-navigation-drawer>

        <v-main style="height: 250px"></v-main>
      </v-layout>
    </v-card>
    <!-- <v-navigation-drawer
      v-model="drawer"
      app
      :temporary="!permanent"
      :permanent="permanent"
      :clipped="false"
      width="300"
      :style="{ top: '64px' }"
    >
      <v-list>
        <router-link
          v-for="item in items"
          :key="item.value"
          :to="item.route"
          custom
          v-slot="{ navigate, isActive }"
        >
          <v-list-item :active="isActive" @click="navigate">
            <v-list-item-title>{{ item.title }}</v-list-item-title>
          </v-list-item>
        </router-link>
      </v-list>
      <template v-slot:append>
        <div class="pa-2">
          <v-btn block @click="drawer = !drawer"> Logout </v-btn>
        </div>
      </template>
    </v-navigation-drawer> -->
    <!-- <v-main>
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/user-data">User Data</RouterLink>
      </nav>
      <RouterView />
    </v-main> -->
    <v-main>
      <router-view></router-view>
    </v-main>
    <teleport to="body">
      <div v-if="showOverlay" class="overlay" @click="closeDrawer"></div>
    </teleport>
  </v-app>
</template>
<style scoped>
nav {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
}

nav a {
  text-decoration: none;
  color: #42b883;
}

nav a:hover {
  color: #38a169;
}

.v-main {
  background-image: url("/path/to/your/background-image.jpg");
  background-size: cover;
  background-position: center;
}

.overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 5;
}
</style>
