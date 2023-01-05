<template>
  <div class="d-flex gap-5 flex-column justify-content-center align-items-center" style="height: 100vh">
    <div>
      <header class="font-bebas text-left d-flex gap-2 flex-row-reverse align-items-center">
        <h1 class="text-white" style="line-height: 80%">
          Untitled <br />
          Chore <br />
          App
        </h1>

        <img src="../assets/icon.svg" alt="" width="140" height="140" />
      </header>

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

const user = useUserStore();
</script>
<style scoped>
header > h1 {
  font-size: 3rem;
}

@media (min-width: 768px) {
  header > img {
    width: 325px;
    height: 325px;
  }

  header > h1 {
    font-size: 8rem;
  }
}
</style>
