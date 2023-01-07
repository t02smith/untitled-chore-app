<template>
  <div>
    <h3 class="text-primary">🏠 Your house:</h3>
    <div class="d-flex flex-column gap-2">
      <div
        v-if="residents"
        v-for="user in residents.sort((a, b) => a.score > b.score)"
        class="px-3 py-1 bg-dark text-light d-flex align-items-center rounded">
        <div class="fw-bold" style="font-size: 1.4rem">
          {{ user.username }}
        </div>
        <strong class="ms-auto text-warning" style="font-size: 1.2rem">{{ user.score.toFixed(2) }}⭐</strong>
      </div>

      <div v-else class="p-1 bg-dark rounded">
        <p class="p-2">loading residents...</p>
      </div>
    </div>
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
