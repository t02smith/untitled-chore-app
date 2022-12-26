<template>
  <div>
    <h3 class="text-primary">Your housemates:</h3>
    <ul class="list-group list-group-flush bg-dark">
      <li
        v-for="user in members"
        class="list-group-item bg-dark text-light row d-flex"
      >
        <p
          class="col-3 text-primary"
          style="font-size: 1.5rem; font-weight: bold"
        >
          {{ user.choresLeft }} to go
        </p>
        <div class="fw-bold col-3" style="font-size: 1.6rem">
          {{ user.username }}
        </div>
        <p class="col-6" style="font-size: 1.1rem">
          {{ "⭐".repeat(user.score) }}
        </p>
      </li>
    </ul>
  </div>
</template>
<script setup>
const members = [
  {
    username: "t02smith",
    score: 8,
    choresLeft: 3,
  },
  {
    username: "tcs1g20",
    score: 5,
    choresLeft: 6,
  },
  {
    username: "jaret",
    score: 9,
    choresLeft: 0,
  },
];
</script>
<style scoped>
p {
  margin-bottom: 0;
}
</style>
