<script setup>
import LoginForm from "./components/LoginForm.vue";
import NavBar from "./components/NavBar.vue";
import { useUserStore } from "./stores/user";

const user = useUserStore();
</script>

<template>
  <div>
    <NavBar />

    <!-- Displays current route -->
    <router-view></router-view>
  </div>
</template>

<style scoped></style>
