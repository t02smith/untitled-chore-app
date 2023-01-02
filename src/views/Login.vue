<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useUserStore } from "../stores/user";

const user = useUserStore();
const router = useRouter();

const username = ref("");
const password = ref("");

const submitted = ref(false);

async function login() {
  submitted.value = true;
  if (username.value.length > 0 && password.value.length > 0) {
    if (await user.login(username.value, password.value)) {
      user.error = "";
      router.push("/home/dashboard");
    }
  } else user.error = "Not enough characters entered";

  submitted.value = false;
}
</script>

<template>
  <form @submit.prevent="login" v-if="!user.accessToken || user.accessToken.value === null">
    <img src="@/assets/logo.png" alt="Image can't be displayed" width="100" height="auto" />

    <h1 class="display-6">Sign in</h1>

    <div class="form-floating mb-3">
      <input type="text" class="form-control" id="username" placeholder="tc3g20" v-model="username" />
      <label for="username" class="form-label">Username</label>
    </div>

    <div class="form-floating mb-3">
      <input type="password" class="form-control" id="passwd" placeholder="password101" v-model="password" />
      <label for="passwd" class="form-label">Password</label>
      <div id="accntHelp" class="form-text">
        Don't have an account?
        <router-link to="/register">Register</router-link>
      </div>
    </div>

    <button type="submit" class="btn btn-primary" :disabled="submitted" v-if="!submitted">Log in</button>
    <div class="spinner-border text-primary" role="status" v-else>
      <span class="sr-only">Loading...</span>
    </div>
  </form>

  <div v-else>You are already logged in</div>
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

div.form-text {
  color: white;
}

h1 {
  margin-top: 0.5em;
  margin-bottom: 1em;
  color: white;
  font-size: 32px;
}
</style>
