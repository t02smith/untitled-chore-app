<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";

const fname = ref("");
const surname = ref("");
const email = ref("");
const username = ref("");
const password = ref("");

const user = useUserStore();
const router = useRouter();

async function register() {
  const res = await user.register(username.value, password.value, fname.value, surname.value, email.value);

  if (res) router.back();
}
</script>

<template>
  <form @submit.prevent="register">
    <img src="@/assets/logo.png" alt="Image can't be displayed" width="100" height="auto" />

    <h1 class="display-6">Register</h1>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="name" placeholder="tc3g20" v-model="fname" />
      <label for="name" class="form-label">First name</label>
    </div>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="surname" placeholder="tc3g20" v-model="surname" />
      <label for="surname" class="form-label">Surname</label>
    </div>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="email" placeholder="tom@gmail.com" v-model="email" />
      <label for="email" class="form-label">emai</label>
    </div>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="username" placeholder="tc3g20" v-model="username" />
      <label for="username" class="form-label">Username</label>
    </div>

    <div class="form-floating mb-3">
      <input type="password" class="form-control" id="passwd" placeholder="password101" v-model="password" />
      <label for="passwd" class="form-label">Password</label>
    </div>

    <button type="submit" class="btn btn-primary">Register</button>
  </form>
</template>

<style scoped>
form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: black;
}

h1 {
  margin-top: 0.5em;
  margin-bottom: 1em;
  color: white;
  font-size: 32px;
}
</style>
