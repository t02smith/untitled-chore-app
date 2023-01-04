<template>
  <div class="container">
    <!-- Home choice and home options -->
    <div class="py-4 px-5 d-flex align-items-center">
      <div class="dropdown">
        <button
          class="btn btn-success dropdown-toggle d-flex align-items-center gap-2"
          style="font-size: 1.5rem"
          type="button"
          id="dropdownMenuButton1"
          data-bs-toggle="dropdown"
          aria-expanded="false">
          <font-awesome-icon icon="fa-solid fa-house" />
          <strong> {{ chosenHome ? `${chosenHome.creator}/${chosenHome.name}` : "loading..." }}</strong>
        </button>
        <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1">
          <li
            v-if="userHomes"
            v-for="h in userHomes.filter((h) => h !== chosenHome.value)"
            @click="() => (chosenHome = h)">
            <a class="dropdown-item d-flex align-items-center gap-2" style="font-size: 1rem" href="#">
              <font-awesome-icon icon="fa-solid fa-house" />
              <strong>{{ h.creator }}/{{ h.name }}</strong></a
            >
            <hr />
          </li>
        </ul>
      </div>

      <div style="margin-left: auto" class="d-flex align-items-center gap-3">
        <button
          v-if="chosenHome"
          type="button"
          class="btn btn-warning"
          data-bs-toggle="modal"
          data-bs-target="#invite-link">
          <strong>Invite</strong>
        </button>

        <button type="button" class="btn btn-success" data-bs-toggle="modal" data-bs-target="#join-home">
          <strong>Join</strong>
        </button>
        <router-link to="/home/create" class="btn btn-success"><strong>Create</strong></router-link>

        <button
          class="bg-transparent"
          :class="refreshing && 'spinner'"
          style="border: none"
          @click="refresh"
          :disabled="refreshing">
          <font-awesome-icon
            icon="fa-solid fa-refresh"
            style="font-size: 2rem"
            class="hover"
            :class="refreshing ? 'text-success' : 'text-muted'" />
        </button>
      </div>
    </div>

    <!-- Page content -->
    <div class="container-fluid px-5">
      <div class="row">
        <HouseMembers class="col-4" :residents="homeResidents" />

        <HouseChoreList class="col-8" :timetable="homeTimetable" :completeChore="complete" />
      </div>
    </div>

    <div
      v-if="chosenHome"
      class="modal fade"
      id="invite-link"
      tabindex="-1"
      aria-labelledby="exampleModalLabel"
      aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" style="width: fit-content; min-width: 60%">
        <HouseInvite :creator="chosenHome.creator" :homeName="chosenHome.name" />
      </div>
    </div>

    <div class="modal fade" id="join-home" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
      <div class="modal-dialog modal-dialog-centered" style="width: fit-content; min-width: 60%">
        <JoinHouse />
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, computed } from "vue";
import HouseMembers from "../../components/House/HouseMembers.vue";
import HouseChoreList from "../../components/House/HouseChoreList.vue";
import JoinHouse from "../../components/House/JoinHouse.vue";
import { useHomeStore } from "../../stores/home";
import { useUserStore } from "../../stores/user";
import HouseInvite from "../../components/House/HouseInvite.vue";
import { useRoute } from "vue-router";

const home = useHomeStore();
const user = useUserStore();

const userHomes = ref([]);

const chosenHome = ref(null);
const homeResidents = ref(null);
const homeTimetable = ref(null);

const refreshing = computed(() => !(userHomes.value && homeResidents.value && homeTimetable.value));

const route = useRoute();

async function refresh() {
  if (user.accessToken === null) return;
  userHomes.value = [];
  homeResidents.value = null;
  homeTimetable.value = null;
  userHomes.value = await home.getHomes();
}

async function complete(id) {
  const res = await home.completeChore(chosenHome.value.creator, chosenHome.value.name, id);
  if (res) {
    refresh();
  }
}

onMounted(() => refresh());

watch(userHomes, () => {
  if (userHomes.value === null || userHomes.value.length === 0) return;

  const selected = userHomes.value.filter((h) => `${h.creator}/${h.name}` === route.query.home);

  chosenHome.value = selected.length === 0 ? userHomes.value[0] : selected[0];
});

watch(chosenHome, async () => {
  if (chosenHome.value === null) return;

  home.getHomeResidents(chosenHome.value.creator, chosenHome.value.name).then((data) => (homeResidents.value = data));
  home.getTimetable(chosenHome.value.creator, chosenHome.value.name).then((data) => (homeTimetable.value = data));
});
</script>
<style scoped>
.spinner {
  animation-name: spin;
  animation-duration: 1500ms;
  animation-iteration-count: infinite;
  animation-timing-function: linear;
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

.hover:hover {
  opacity: 0.75;
  transition: 150ms;
}
</style>
