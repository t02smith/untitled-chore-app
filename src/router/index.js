import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import CreateHome from "../views/home/CreateHome.vue";
import HomeDashboard from "../views/home/HomeDashboard.vue";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "login",
      component: Login,
    },
    {
      path: "/register",
      name: "register",
      component: Register,
    },
    {
      path: "/home/dashboard",
      name: "home-dashboard",
      component: HomeDashboard,
    },
    {
      path: "/home/create",
      name: "create-home",
      component: CreateHome,
    },
  ],
});

export default router;
