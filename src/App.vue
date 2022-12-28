<script setup>
import LoginForm from "./components/LoginForm.vue";
import NavBar from "./components/NavBar.vue";
import { useUserStore } from "./stores/user";

const user = useUserStore();
</script>

<template>
  <div>
    <NavBar />

    <div v-if="!user.user">
      <LoginForm />
    </div>

    <!-- Displays current route -->
    <router-view v-else></router-view>
  </div>
</template>

<style scoped></style>
