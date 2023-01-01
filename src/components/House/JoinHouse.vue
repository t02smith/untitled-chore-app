<template>
  <div class="modal-content bg-dark">
    <div class="modal-header">
      <h4 class="modal-title text-success">🏠 Join a New Home</h4>
    </div>

    <form @submit.prevent="join">
      <div class="modal-body">
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
              placeholder="who created the house"
              aria-describedby="helpId"
              v-model="joinId" />
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-success" type="submit"><strong> Join </strong></button>
        <button type="button" class="btn btn-danger" data-dismiss="modal"><strong> Close </strong></button>
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

async function join() {
  await home.joinHome(creator.value, name.value, joinId.value);
}
</script>
