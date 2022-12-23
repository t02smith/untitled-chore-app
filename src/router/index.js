import { createRouter, createWebHistory } from "vue-router";
import Login from "../views/Login.vue";
import Register from "../views/Register.vue";
import Home from "../views/Home.vue";
import Chores from "../views/Chores.vue";
import Group from "../views/Group.vue";
import Help from "../views/Help.vue";
import User from "../views/User.vue";

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
            path: "/home",
            name: "home",
            component: Home,
        },
        {
            path: "/group",
            name: "group",
            component: Group,
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
