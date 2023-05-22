<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Error from "../components/Error.vue";
import TitleCard from "../components/TitleCard.vue";
import { useUserStore } from "../stores/user";

const fname = ref("");
const surname = ref("");
const email = ref("");
const username = ref("");
const password = ref("");
const password2 = ref("");

const user = useUserStore();
const router = useRouter();

const submitted = ref(false);

async function register() {
  submitted.value = true;
  if (password.value !== password2.value) {
    user.error = "passwords do not match";
    return;
  }
  const res = await user.register(username.value, password.value, fname.value, surname.value, email.value);

  submitted.value = false;
  if (res) router.back();
}
</script>

<template>
  <div class="wrapper mx-5">
    <TitleCard class="title" />

    <form @submit.prevent="register" class="d-flex flex-column align-items-center">
      <h1 class="display-6 text-white text-center">Join <strong> Untitled Chore App </strong> today</h1>
      <p class="form-text text-center" style="margin-top: -0.5rem; font-size: 1.1rem">
        Already have an account?
        <router-link to="/login">Login now!</router-link>
      </p>

      <Error class="container mx-3" />

      <div class="d-flex flex-column">
        <h5 class="mb-0 text-white">About you</h5>
        <hr class="mb-3" />

        <div class="row g-2">
          <div class="col form-floating mb-3">
            <input type="text" class="form-control" id="name" placeholder="tc3g20" v-model="fname" />
            <label for="name" class="form-label">First name</label>
          </div>

          <div class="col form-floating mb-3">
            <input type="text" class="form-control" id="surname" placeholder="tc3g20" v-model="surname" />
            <label for="surname" class="form-label">Surname</label>
          </div>
        </div>

        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="email" placeholder="tom@gmail.com" v-model="email" />
          <label for="email" class="form-label">Email</label>
        </div>

        <h5 class="mb-0 text-white">Your account</h5>
        <hr class="mb-3" />

        <div class="form-floating mb-3">
          <input type="text" class="form-control" id="username" placeholder="tc3g20" v-model="username" />
          <label for="username" class="form-label">Username</label>
        </div>

        <div class="row g-2 mb-3">
          <div class="form-floating col">
            <input type="password" class="form-control" id="passwd" placeholder="password101" v-model="password" />
            <label for="passwd" class="form-label">Password</label>
          </div>

          <div class="form-floating col">
            <input type="password" class="form-control" id="passwd" placeholder="password101" v-model="password2" />
            <label for="passwd" class="form-label">Repeat Password</label>
          </div>
        </div>

        <hr class="mb-3" />
        <button :disabled="submitted" type="submit" class="btn btn-primary">Register</button>
      </div>
    </form>
  </div>
</template>

<style scoped>
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

form {
  color: black;
}

hr {
  margin-top: 5px;
  margin-bottom: 5px;
  border-color: white;
  border-width: 2px;
}
</style>
