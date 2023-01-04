div
<template>
  <div>
    <div class="d-flex align-items-center">
      <h3 class="text-primary">Still to do:</h3>
      <h3 style="margin-left: auto" class="text-muted">{{ daysLeft }} days left</h3>
    </div>

    <div class="d-flex flex-column gap-1" v-if="props.timetable && user.user">
      <ChoreCard
        v-if="props.timetable.tasks.filter((t) => !t.complete).length === 0"
        name="No chores left to do"
        color="green"
        icon="fa-solid fa-square-check"
        room="good job!" />

      <ChoreCard
        v-else
        v-for="c in props.timetable.tasks
          .filter((t) => !t.complete)
          .sort((a, b) => (a.assigned_to < b.assigned_to ? -1 : 1))"
        :name="c.chore.name"
        :username="c.assigned_to"
        :room="c.chore.room.name"
        :color="c.chore.room.colour"
        :icon="c.chore.room.icon" />
    </div>

    <div v-else class="p-1 bg-dark rounded">
      <p class="p-2">loading tasks...</p>
    </div>
  </div>
</template>
<script setup>
import { onMounted, computed } from "vue";
import { useUserStore } from "../../stores/user";
import ChoreCard from "../ChoreCard.vue";

const user = useUserStore();

onMounted(() => {
  if (!user.user) user.getUserData();
});

const props = defineProps({
  timetable: {
    required: true,
  },
});

const daysLeft = computed(() =>
  props.timetable ? Math.ceil((new Date(props.timetable.end).getTime() - new Date().getTime()) / (1000 * 3600 * 24)) : 0
);
</script>
