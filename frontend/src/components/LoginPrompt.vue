<template>
  <div class="container mt-3">
    <div class="alert alert-secondary">
      <h6 class="alert-heading">⚠️ You aren't logged in!</h6>
      <hr />
      <p>To use <strong>Untitled Chore App</strong> you need to sign in or create an account.</p>
      <div class="d-flex align-items-center gap-2">
        <button @click="router.push('/login')" class="btn btn-danger">Login</button>
        <button @click="router.push('/register')" class="btn btn-success">Register</button>
      </div>
    </div>
  </div>
</template>
<script setup>
import { useRouter } from "vue-router";

const router = useRouter();
</script>
