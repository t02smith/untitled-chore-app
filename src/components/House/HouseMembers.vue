<template>
  <div>
    <h3 class="text-primary">Your house:</h3>
    <ul class="list-group list-group-flush bg-dark">
      <li
        v-if="residents"
        v-for="user in residents"
        class="list-group-item bg-dark text-light row d-flex align-items-center">
        <div class="fw-bold col-6" style="font-size: 1.4rem">
          {{ user.username }}
        </div>
        <p class="col-6 ms-auto" style="font-size: 1rem">
          {{ "⭐".repeat(3) }}
        </p>
      </li>

      <div v-else class="p-1 bg-dark rounded" style="border-collapse: separate">
        <p class="p-2">loading residents...</p>
      </div>
    </ul>
  </div>
</template>
<script setup>
const props = defineProps({
  residents: {
    default: null,
  },
});
</script>
<style scoped>
p {
  margin-bottom: 0;
}
</style>
