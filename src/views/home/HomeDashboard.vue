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
          aria-expanded="false"
        >
          <font-awesome-icon icon="fa-solid fa-house" />
          <strong> {{ chosenHome }} </strong>
        </button>
        <ul
          class="dropdown-menu dropdown-menu-dark"
          aria-labelledby="dropdownMenuButton1"
        >
          <li
            v-for="h in homes.filter((h) => h !== chosenHome)"
            @click="chosenHome = h"
          >
            <a
              class="dropdown-item d-flex align-items-center gap-2"
              style="font-size: 1.5rem"
              href="#"
            >
              <font-awesome-icon icon="fa-solid fa-house" />
              <strong>{{ h }}</strong></a
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
        <HouseMembers class="col" />

        <HouseChoreList class="col-6" />

        <div class="col"></div>
      </div>
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted } from "vue";
import HouseMembers from "../../components/House/HouseMembers.vue";
import HouseChoreList from "../../components/House/HouseChoreList.vue";
import { useHomeStore } from "../../stores/home";

const home = useHomeStore();

onMounted(async () => await home.getHome("t02smith", "myhome"));

const homes = ref(["Home", "Parent's", "The Boys"]);

const chosenHome = ref("Home");
</script>
