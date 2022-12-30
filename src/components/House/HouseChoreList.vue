div
<template>
  <div>
    <div class="d-flex align-items-center">
      <h3 class="text-primary">Still to do:</h3>
      <h3 style="margin-left: auto" class="text-muted">3 days left</h3>
    </div>

    <div class="d-flex flex-column gap-1" v-if="props.timetable">
      <ChoreCard
        v-for="c in props.timetable.tasks.filter((t) => !t.complete)"
        :name="c.chore.name"
        :username="c.assigned_to"
        room="bathroom"
        color="#0ac"
        icon="fa fa-shower" />
    </div>

    <div v-else class="p-1 bg-dark rounded">
      <p class="p-2">loading tasks...</p>
    </div>
  </div>
</template>
<script setup>
import ChoreCard from "../ChoreCard.vue";

const props = defineProps({
  timetable: {
    required: true,
  },
});
</script>
