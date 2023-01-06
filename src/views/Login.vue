<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Error from "../components/Error.vue";
import TitleCard from "../components/TitleCard.vue";
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
  <div class="wrapper mx-5">
    <TitleCard />

    <form
      @submit.prevent="login"
      v-if="!user.accessToken || user.accessToken.value === null"
      class="d-flex flex-column align-items-center">
      <h1 class="display-6 text-white text-center">Sign into <strong> Untitled Chore App </strong></h1>
      <p class="form-text text-center" style="margin-top: -0.5rem; font-size: 1.1rem">
        Don't have an account?
        <router-link to="/register">Join us today!</router-link>
      </p>

      <Error class="container mx-3" />

      <div style="max-width: 75%" class="d-flex flex-column align-items-center">
        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="username" placeholder="tc3g20" v-model="username" />
          <label for="username" class="form-label">Username</label>
        </div>

        <div class="form-floating mb-3">
          <input type="password" class="form-control" id="passwd" placeholder="password101" v-model="password" />
          <label for="passwd" class="form-label">Password</label>
        </div>

        <button type="submit" class="btn btn-primary" :disabled="submitted" v-if="!submitted">Log in</button>
        <div class="spinner-border text-primary" role="status" v-else>
          <span class="sr-only"></span>
        </div>
      </div>
    </form>

    <div v-else class="d-flex flex-column align-items-center gap-4">
      <h1>You're already logged in!</h1>
      <div class="d-flex gap-3">
        <router-link to="/home/dashboard" class="btn btn-primary">Your Dashboard</router-link>
        <button class="btn btn-danger" @click="user.logout">Logout</button>
      </div>
    </div>
  </div>
</template>
<style scoped>
form {
  color: black;
}

@media (max-width: 1200px) {
  .title-card {
    display: none;
  }

  .wrapper {
    grid-template-columns: 1fr;
  }
}

@media (min-width: 1200px) {
  .wrapper {
    grid-template-columns: 1fr 1fr;
  }
}

.wrapper {
  display: grid;
  place-items: center;
  height: 80vh;
}
</style>
