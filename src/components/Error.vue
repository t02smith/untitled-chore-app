<template>
  <div v-if="user.error">
    <div class="alert alert-danger">
      <h6 class="alert-heading">❌ {{ user.error }}</h6>
    </div>
  </div>
</template>
<script setup>
import { useUserStore } from "../stores/user";

const user = useUserStore();
</script>
