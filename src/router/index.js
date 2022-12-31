import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Chores from "../views/Chores.vue";
import Help from "../views/Help.vue";
import User from "../views/User.vue";
import HomeDashboard from "../views/home/HomeDashboard.vue";
import CreateHome from "../views/home/CreateHome.vue";

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
        {
            path: "/chores",
            name: "chores",
            component: Chores,
        },
        {
            path: "/help",
            name: "help",
            component: Help,
        },
        {
            path: "/user",
            name: "user",
            component: User,
        },
    ],
});

export default router;
