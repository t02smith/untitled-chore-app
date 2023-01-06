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

router.afterEach((to, from, failure) => {
  user.error = null;
});

// if (!user.accessToken && path !== "/login" && path !== "/register") {
//   router.push("/");
// }
</script>

<template>
  <div>
    <NavBar v-if="path !== '/'" />

    <LoginPrompt v-if="!user.accessToken && !['/', '/login', '/register'].includes(path)" />

    <Error class="container my-3" v-if="!['/login', '/register'].includes(path)" />

    <!-- Displays current route -->
    <main>
      <router-view />
    </main>
  </div>
</template>
