import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../components/HomePage.vue";
import UserDataView from "../views/UserDataView.vue";
import UserTimesheetView from "../views/UserTimesheetView.vue";
import AdminUserView from "../views/AdminUsers.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  // {
  //   path: "",
  //   name: "AdminUsers",
  //   component: AdminUserView,
  // },
  {
    path: "/user-data",
    name: "UserData",
    component: UserDataView,
  },
  {
    path: "/time-sheet",
    name: "TimeSheet",
    component: UserTimesheetView,
  },

  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("../views/NotFound.vue"),
  },
  // Add other routes as needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
