<template>
  <div class="container p-4" v-if="!homeCreated">
    <div class="jumbotron bg-dark p-4 my-4 shadow rounded">
      <h1 class="display-2 text-primary font-weight-bold">Create a new home!</h1>
      <p class="lead">
        Choose a house name, your choice of chores made by us, which friends you want to invite and create your house
        now to jumpstart your productivity!
      </p>
    </div>

    <form @submit.prevent="createHome" class="d-flex flex-column gap-5" style="max-width: 992px">
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
          class="form-control mb-2"
          placeholder="e.g. myhome"
          aria-describedby="helpId"
          v-model="houseName" />

        <p v-if="houseName.length === 0"></p>

        <p v-else-if="userHomes.includes(houseName)" class="text-danger">
          ❌ You already have a house called <strong> {{ houseName }} </strong>
        </p>

        <p v-else class="text-success">
          ✅ <strong> {{ houseName }} </strong> is available
        </p>
      </div>

      <div class="form-group">
        <label for="" class="h5 text-primary">Pick some basic chores:</label>
        <p class="text-muted" style="margin-top: -0.5rem">Or design your own once you've created your house</p>
        <div class="chore-options">
          <ChoreCard
            v-if="defaultChores"
            v-for="c in defaultChores"
            :name="c.name"
            :expectedTime="c.expected_time"
            :room="c.room.name"
            :color="c.room.colour"
            :icon="c.room.icon"
            :difficulty="c.difficulty"
            style="width: 20rem">
            <input
              type="checkbox"
              name=""
              id=""
              class="form-check-input ms-2 bg-secondary justify-self-end"
              style="width: 2rem; height: 2rem"
              @click="() => toggleChore(c.id)" />
          </ChoreCard>

          <ChoreCard
            v-else
            name="Loading default chores..."
            color="#fff"
            icon="fa fa-shower"
            room=""
            style="width: 20rem" />
        </div>
      </div>

      <button
        v-if="!submitted"
        :disabled="submitted"
        type="submit"
        class="btn btn-success btn-lg"
        style="width: fit-content">
        Create
      </button>
      <div class="spinner-border text-primary" role="status" v-else>
        <span class="sr-only">Loading...</span>
      </div>
    </form>
  </div>

  <HouseInvite v-else :creator="homeCreated.creator" :homeName="homeCreated.name" title="Home Created!" showLink />
</template>
<script setup>
import { ref, onMounted } from "vue";
import ChoreCard from "../../components/ChoreCard.vue";
import { useHomeStore } from "../../stores/home";
import { useChoreStore } from "../../stores/chores";
import { useUserStore } from "../../stores/user";
import HouseInvite from "../../components/House/HouseInvite.vue";

const home = useHomeStore();
const chores = useChoreStore();
const user = useUserStore();

const defaultChores = ref(null);
const userHomes = ref([]);

const houseName = ref("");
const chosenChores = ref([]);

const inviteLink = ref(null);
const homeCreated = ref(null);

const submitted = ref(false);

const toggleChore = (id) =>
  chosenChores.value.includes(id)
    ? (chosenChores.value = chosenChores.value.filter((c) => c !== id))
    : chosenChores.value.push(id);

async function createHome() {
  submitted.value = true;
  const res = await home.createHome(houseName.value, chosenChores.value);
  submitted.value = false;
  if (!res) return;

  homeCreated.value = res;
  inviteLink.value = await home.createInviteLink(res.creator, res.name);
}

onMounted(async () => {
  if (user.accessToken === null) return;
  chores.getDefaultChores().then((data) => (defaultChores.value = data));
  home.getHomes().then((data) => {
    if (data === null) return;
    userHomes.value = data.map((c) => c.name);
  });
});
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
