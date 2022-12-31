<script setup>
import NavBar from "./components/NavBar.vue";
import LoginPrompt from "./components/LoginPrompt.vue";
import { useUserStore } from "./stores/user";
import { useRoute } from "vue-router";
import { computed } from "vue";
import router from "./router";

const user = useUserStore();
const route = useRoute();
const path = computed(() => route.path);

if (!user.accessToken && path !== '/login' && path !== '/register') {
    router.push('/');
}
</script>

<template>
  <div>
    <NavBar />

    <!-- <LoginPrompt v-if="!user.accessToken && path !== '/login' && path !== '/register'" /> -->

    <div class="container my-3" v-if="user.error">
      <div class="alert alert-danger">
        <h6 class="alert-heading">❌ {{ user.error }}</h6>
      </div>
    </div>

    <!-- Displays current route -->
    <router-view />
  </div>
</template>

<style scoped></style>
