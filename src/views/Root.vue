<template>
  <div class="d-flex gap-5 flex-column justify-content-center align-items-center" style="height: 100vh">
    <div>
      <TitleCard />

      <div
        class="bg-dark mx-2 px-3 py-2 text-center rounded shadow text-white d-flex align-items-center justify-content-center">
        <h5 style="margin-bottom: 0">🎯 Kickstart your productivity today!</h5>
        <router-link :to="user.accessToken ? '/home/dashboard' : '/login'" class="ms-auto btn btn-success py-1"
          >Go</router-link
        >
      </div>
    </div>
  </div>
</template>
<script setup>
import { useUserStore } from "../stores/user";
import TitleCard from "../components/TitleCard.vue";

const user = useUserStore();
</script>
