<template>
  <div>
    <div class="d-flex align-items-center">
      <h3 class="text-primary">Still to do:</h3>
      <h3 style="margin-left: auto" class="text-muted">3 days left</h3>
    </div>

    <div class="d-flex flex-column gap-1">
      <ChoreCard
        v-for="c in chores"
        :name="c.name"
        :username="c.username"
        :room="c.room"
        :color="c.color"
        :icon="c.icon"
      />
    </div>
  </div>
</template>
<script setup>
import ChoreCard from "../ChoreCard.vue";

const chores = [
  {
    id: 0,
    name: "Clean the Shower",
    username: "t02smith",
    room: "Bathroom",
    color: "#0ac",
    icon: "fa fa-shower",
  },
  {
    id: 1,
    name: "Do the Dishes",
    username: "t02smith",
    room: "Kitchen",
    color: "#F24E1E",
    icon: "fa-solid fa-kitchen-set",
  },
  {
    id: 2,
    name: "Hoover",
    username: "t02smith",
    room: "Living Room",
    color: "#0FA958",
    icon: "fa-solid fa-couch",
  },
  {
    id: 3,
    name: "Take the Bins Out",
    username: "t02smith",
    room: "Kitchen",
    color: "#F24E1E",
    icon: "fa-solid fa-kitchen-set",
  },
  {
    id: 4,
    name: "Tidy Up",
    room: "Living Room",
    username: "t02smith",
    color: "#0FA958",
    icon: "fa-solid fa-couch",
  },
  {
    id: 5,
    name: "Clean the Toilet",
    room: "Bathroom",
    username: "t02smith",
    color: "#0ac",
    icon: "fa fa-shower",
  },
];
</script>
