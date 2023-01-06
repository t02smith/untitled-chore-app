<script setup>
import NavBar from "./components/Navbar.vue";
import LoginPrompt from "./components/LoginPrompt.vue";
import { useUserStore } from "./stores/user";
import { useRoute } from "vue-router";
import { computed } from "vue";
import router from "./router";

const user = useUserStore();
const route = useRoute();
const path = computed(() => route.path);

if (!user.accessToken && path !== '/' && path !== '/register') {
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

    <!-- Displays current route with fade transition-->
    <router-view v-slot="{ Component }">
      <Transition name="page-opacity" mode="out-in">
        <component :is="Component"></component>
      </Transition>
    </router-view>
  </div>
</template>

<style scoped>
.page-opacity-enter-active,
.page-opacity-leave-active {
  transition: 300ms ease all;
}

.page-opacity-enter-from,
.page-opacity-leave-to {
  opacity: 0;
}
</style>
