<template>
  <div class="modal-content bg-dark">
    <div class="modal-header">
      <h4 class="modal-title text-success">🏠 Join a New Home</h4>
    </div>

    <form @submit.prevent="join">
      <div class="modal-body">
        <div class="alert alert-success" v-if="success">
          <h6 class="alert-heading">✅ Home joined successfully</h6>
        </div>

        <Error />

        <div class="container d-flex flex-column gap-3">
          <div class="form-group">
            <label for="" class="text-white">🧑‍🦱Home Owner:</label>
            <input
              type="text"
              name=""
              id=""
              class="form-control"
              placeholder="e.g. tcs1g20"
              aria-describedby="helpId"
              v-model="creator" />
          </div>

          <div class="form-group">
            <label for="" class="text-white"> 🔎 Home Name:</label>
            <input
              type="text"
              name=""
              id=""
              class="form-control"
              placeholder="e.g. home"
              aria-describedby="helpId"
              v-model="name" />
          </div>

          <div class="form-group">
            <label for="" class="text-white">🔐 Invite Code:</label>
            <input
              type="text"
              name=""
              id=""
              class="form-control"
              placeholder="The secret invite code to the house"
              aria-describedby="helpId"
              v-model="joinId" />
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-success" type="submit" :disabled="submitted" v-if="!submitted">
          <strong> Join </strong>
        </button>
        <div v-else class="spinner-border text-success" role="status">
          <span class="sr-only">Loading...</span>
        </div>
      </div>
    </form>
  </div>
</template>
<script setup>
import { ref } from "vue";
import { useHomeStore } from "../../stores/home";
import Error from "../Error.vue";

const creator = ref("");
const name = ref("");
const joinId = ref("");

const home = useHomeStore();

const success = ref(false);
const submitted = ref(false);

async function join() {
  submitted.value = true;
  success.value = false;
  const res = await home.joinHome(creator.value, name.value, joinId.value);

  joinId.value = "";
  if (res) {
    creator.value = "";
    name.value = "";
    success.value = true;
  }
  submitted.value = false;
}
</script>
