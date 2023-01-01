<script setup>
import NavBar from "./components/Navbar.vue";
import LoginPrompt from "./components/LoginPrompt.vue";
import { useUserStore } from "./stores/user";
import { useRoute } from "vue-router";
import { computed } from "vue";
import router from "./router";
import Error from "./components/Error.vue";

const user = useUserStore();
const route = useRoute();
const path = computed(() => route.path);

// if (!user.accessToken && path !== "/login" && path !== "/register") {
//   router.push("/");
// }
</script>

<template>
  <div>
    <NavBar />

    <LoginPrompt v-if="!user.accessToken && path !== '/login' && path !== '/register'" />

    <Error class="container my-3" />

    <!-- Displays current route -->
    <main>
      <router-view />
    </main>
  </div>
</template>

<style scoped></style>
