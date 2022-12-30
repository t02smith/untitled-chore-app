<template>
  <div>
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

      <div style="margin-left: auto">
        <a :href="`/home/settings?home=${chosenHome}`">
          <font-awesome-icon icon="fa-solid fa-gear" style="font-size: 2rem" />
        </a>
      </div>
    </div>

    <!-- Page content -->
    <div class="container-fluid px-5">
      <div class="row">
        <HouseMembers class="col" :residents="homeResidents" />

        <HouseChoreList class="col-6" :timetable="homeTimetable" />

        <div class="col"></div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch } from "vue";
import HouseMembers from "../../components/House/HouseMembers.vue";
import HouseChoreList from "../../components/House/HouseChoreList.vue";
import { useHomeStore } from "../../stores/home";

const home = useHomeStore();

const userHomes = ref([]);

const chosenHome = ref(null);
const homeResidents = ref(null);
const homeTimetable = ref(null);

onMounted(async () => (userHomes.value = await home.getHomes()));

watch(userHomes, () => {
  if (userHomes.value === null || userHomes.value.length === 0) return;
  chosenHome.value = userHomes.value[0];
});

watch(chosenHome, async () => {
  homeResidents.value = null;
  homeTimetable.value = null;

  if (chosenHome.value === null) return;

  home.getHomeResidents(chosenHome.value.creator, chosenHome.value.name).then((data) => (homeResidents.value = data));

  home.getTimetable(chosenHome.value.creator, chosenHome.value.name).then((data) => (homeTimetable.value = data));
});
</script>
