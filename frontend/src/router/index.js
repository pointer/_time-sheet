import { createRouter, createWebHistory } from "vue-router";
import HomeView from "../components/HomePage.vue";
import LoginView from "../components/LoginView.vue";
import UserDataView from "../views/UserDataView.vue";
import UserTimesheetView from "../views/UserTimesheetView.vue";
import AdminUserView from "../views/AdminUsers.vue";
import SupervisorView from "../views/SupervisorView.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomeView,
  },
  {
    path: "/login",
    name: "Login",
    component: LoginView,
  },
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
    path: "/supervisor",
    name: "Supervisor",
    component: SupervisorView,
  },  
  {
    path: "/:pathMatch(.*)*",
    name: "NotFound",
    component: () => import("../components/NotFound.vue"),
  },
  // Add other routes as needed
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

router.beforeEach((to, from, next) => {
  const user = JSON.parse(localStorage.getItem('user'));
  if (to.meta.role && (!user || user.role !== to.meta.role)) {
    next('/login');
  } else {
    next();
  }
});

export default router;
