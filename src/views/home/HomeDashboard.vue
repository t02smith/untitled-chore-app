<template>
  <div class="container">
    <!-- Home choice and home options -->
    <div class="py-4 px-5 d-flex align-items-center">
      <div class="dropdown">
        <button
          class="btn btn-dark dropdown-toggle d-flex align-items-center gap-2"
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
            @click="
              () => {
                chosenHome = h;
                router.replace({ path: route.path, query: { home: h.name } });
              }
            ">
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
          class="bg-transparent mt-1"
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

        <div class="dropdown">
          <button
            class="bg-transparent text-white d-flex align-items-center gap-2"
            style="font-size: 1.5rem; border: none; font-size: 2rem"
            type="button"
            id="dropdownMenuButton1"
            data-bs-toggle="dropdown"
            aria-expanded="false">
            <font-awesome-icon icon="fa-solid fa-bars" />
          </button>
          <ul class="dropdown-menu dropdown-menu-dark" aria-labelledby="dropdownMenuButton1">
            <button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#invite-link" :disabled="!chosenHome">
              🫂 Invite others
            </button>
            <button class="dropdown-item" data-bs-toggle="modal" data-bs-target="#join-home">🏡 Join home</button>
            <router-link to="/home/create" class="dropdown-item">🆕 Create home</router-link>

            <div v-if="chosenHome">
              <hr />
              <div v-if="chosenHome.creator !== user.user.username">
                <button class="dropdown-item" @click="leaveHome">⚠️ Leave home</button>
              </div>
              <div v-else>
                <button class="dropdown-item" @click="regenerateTimetable">♻️ Regenerate timetable</button>
                <button class="dropdown-item" @click="deleteHome">🗑️ Delete home</button>
              </div>
            </div>
          </ul>
        </div>
      </div>
    </div>

    <!-- Page content -->
    <div class="container-fluid px-5 pb-4">
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
      <div class="modal-dialog modal-dialog-centered" style="width: 500px">
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
import { useRoute, useRouter } from "vue-router";

const home = useHomeStore();
const user = useUserStore();

const userHomes = ref([]);

const chosenHome = ref(null);
const homeResidents = ref(null);
const homeTimetable = ref(null);

const refreshing = computed(() => !(userHomes.value && homeResidents.value && homeTimetable.value));

const route = useRoute();
const router = useRouter();

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

async function leaveHome() {
  await home.leaveHome(chosenHome.value.creator, chosenHome.value.name);
  refresh();
}

async function deleteHome() {
  await home.deleteHome(chosenHome.value.creator, chosenHome.value.name);
  refresh();
}

async function regenerateTimetable() {
  homeResidents.value = null;
  homeTimetable.value = null;
  home.getHomeResidents(chosenHome.value.creator, chosenHome.value.name).then((data) => (homeResidents.value = data));
  home.getTimetable(chosenHome.value.creator, chosenHome.value.name, true).then((data) => (homeTimetable.value = data));
}

onMounted(() => refresh());

watch(userHomes, () => {
  if (userHomes.value === null || userHomes.value.length === 0) return;

  const selected = userHomes.value.filter((h) => `${h.creator}/${h.name}` === route.query.home);
  chosenHome.value = selected.length === 0 ? userHomes.value[0] : selected[0];
});

watch(chosenHome, async () => {
  homeResidents.value = null;
  homeTimetable.value = null;
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
