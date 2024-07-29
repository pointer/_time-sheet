import { createApp } from "vue";
import { createPinia } from "pinia";
import "./style.css";
import App from "./App.vue";
import router from "./router";
import vuetify from "./plugins/vuetify";
import dotenv from "dotenv";

// dotenv.config({ path: "../.env" });
// console.log(process.env); // remove this after you've confirmed it is working
console.log(import.meta.env.APP_API_URL); // "123"
console.log(import.meta.env.VUE_APP_API_URL); // undefined
// console.log(process.env.NODE_ENV, process.env.PORT);
// import "./addRequire.js";
// app.use(createPinia());
createApp(App).use(createPinia()).use(router).use(vuetify).mount("#app");
