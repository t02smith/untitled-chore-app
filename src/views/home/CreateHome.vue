<template>
  <div class="container p-4">
    <div class="jumbotron bg-dark p-4 my-4 shadow rounded">
      <h1 class="display-2 text-primary font-weight-bold">
        Create a new home!
      </h1>
      <p class="lead">
        Choose a house name, your choice of chores made by us, which friends you
        want to invite and create your house now to jumpstart your productivity!
      </p>
    </div>

    <form
      @submit.prevent=""
      class="d-flex flex-column gap-5"
      style="max-width: 992px"
    >
      <div class="form-group">
        <label for="" class="h5 text-primary">Your house name:</label>
        <p id="helpId" class="text-muted" style="margin-top: -0.5rem">
          This has to be different from all your other houses
        </p>
        <div class="d-flex gap-2"></div>
        <input
          type="text"
          name=""
          id=""
          class="form-control"
          placeholder="e.g. myhome"
          aria-describedby="helpId"
          v-model="houseName"
        />
      </div>

      <div class="form-group">
        <label for="" class="h5 text-primary">Pick some basic chores:</label>
        <p class="text-muted" style="margin-top: -0.5rem">
          Or design your own once you've created your house
        </p>
        <div class="chore-options">
          <ChoreCard
            v-for="c in chores"
            :name="c.name"
            :room="c.room"
            :color="c.color"
            :icon="c.icon"
            :onToggle="() => toggleChore(c.id)"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="" class="h5 text-primary">Invite some friends:</label>
        <p class="text-muted" style="margin-top: -0.5rem">
          Sent your housemates an invite to join once your house is created
        </p>
        <form class="input-group mb-3" @submit.prevent="newUser">
          <span class="input-group-text" id="basic-addon1">@</span>
          <input
            type="text"
            class="form-control"
            placeholder="Username"
            v-model="userToInvite"
            @submit="console.log('hello')"
          />

          <button type="submit" class="btn btn-primary">Invite</button>
        </form>

        <div class="d-flex gap-2">
          <button
            class="btn btn-primary font-weight-bold px-2 py-1"
            @click="() => removeUser(user)"
            v-for="user in invitedUsers"
          >
            <small>{{ user }}</small>
          </button>
        </div>
      </div>

      <button
        type="submit"
        class="btn btn-success btn-lg"
        style="width: fit-content"
      >
        Create
      </button>
    </form>
  </div>
</template>
<script setup>
import { ref } from "vue";
import ChoreCard from "../../components/ChoreCard.vue";

const houseName = ref("");
const chosenChores = ref([]);

const userToInvite = ref("");
const invitedUsers = ref([]);

const newUser = () => {
  invitedUsers.value.push(userToInvite.value);
  userToInvite.value = "";
};
const removeUser = (rm) =>
  (invitedUsers.value = invitedUsers.value.filter((u) => u !== rm));

const toggleChore = (id) =>
  chosenChores.value.includes(id)
    ? (chosenChores.value = chosenChores.value.filter((c) => c !== id))
    : chosenChores.value.push(id);

const chores = [
  {
    id: 0,
    name: "Clean the Shower",
    room: "Bathroom",
    color: "#0ac",
    icon: "fa fa-shower",
  },
  {
    id: 1,
    name: "Do the Dishes",
    room: "Kitchen",
    color: "#F24E1E",
    icon: "fa-solid fa-kitchen-set",
  },
  {
    id: 2,
    name: "Hoover",
    room: "Living Room",
    color: "#0FA958",
    icon: "fa-solid fa-couch",
  },
  {
    id: 3,
    name: "Take the Bins Out",
    room: "Kitchen",
    color: "#F24E1E",
    icon: "fa-solid fa-kitchen-set",
  },
  {
    id: 4,
    name: "Tidy Up",
    room: "Living Room",
    color: "#0FA958",
    icon: "fa-solid fa-couch",
  },
  {
    id: 5,
    name: "Clean the Toilet",
    room: "Bathroom",
    color: "#0ac",
    icon: "fa fa-shower",
  },
];

// TODO fetch users existing house names to validate new house name
// TODO fetch default chores from api
</script>
<style scoped>
input[type="text"] {
  max-width: 600px;
}

.chore-options {
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  gap: 1rem;
  place-items: center;
}
</style>
