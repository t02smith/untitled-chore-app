div
<template>
  <div>
    <div class="d-flex align-items-center">
      <h3 class="text-primary">👇 Still to do:</h3>
      <h3 style="margin-left: auto" class="text-muted">🗓️ {{ daysLeft }} days left</h3>
    </div>

    <div class="d-flex flex-column gap-2" v-if="props.timetable && user.user">
      <ChoreCard
        v-if="props.timetable.tasks.filter((t) => !t.complete).length === 0"
        name="No chores left to do"
        color="green"
        icon="fa-solid fa-square-check"
        room="good job!" />

      <ChoreCard
        v-for="c in props.timetable.tasks.filter((t) => !t.complete && t.assigned_to === user.user.username)"
        :name="c.chore.name"
        :username="c.assigned_to"
        :room="c.chore.room.name"
        :color="c.chore.room.colour"
        :icon="c.chore.room.icon"
        :expectedTime="c.chore.expected_time"
        :difficulty="c.chore.difficulty">
        <button
          v-if="props.completeChore"
          class="bg-dark hover"
          style="border: none; font-size: 2rem"
          @click="() => complete(c.chore.id)"
          :disabled="submitted">
          ✅
        </button>
      </ChoreCard>

      <ChoreCard
        v-for="c in props.timetable.tasks
          .filter((t) => !t.complete && t.assigned_to !== user.user.username)
          .sort((a, b) => (a.assigned_to < b.assigned_to ? -1 : 1))"
        :name="c.chore.name"
        :username="c.assigned_to"
        :room="c.chore.room.name"
        :color="c.chore.room.colour"
        :icon="c.chore.room.icon"
        :expectedTime="c.chore.expected_time"
        :difficulty="c.chore.difficulty" />
    </div>

    <div v-else class="p-1 bg-dark rounded">
      <p class="p-2">loading tasks...</p>
    </div>
  </div>
</template>
<script setup>
import { onMounted, computed, ref } from "vue";
import { useUserStore } from "../../stores/user";
import ChoreCard from "../ChoreCard.vue";

const user = useUserStore();

const submitted = ref(false);

onMounted(() => {
  if (!user.user) user.getUserData();
});

const props = defineProps({
  timetable: {
    required: true,
  },
  completeChore: {
    type: Function,
    required: false,
  },
});

async function complete(id) {
  submitted.value = true;
  await props.completeChore(id);
  submitted.value = false;
}

const daysLeft = computed(() =>
  props.timetable ? Math.ceil((new Date(props.timetable.end).getTime() - new Date().getTime()) / (1000 * 3600 * 24)) : 0
);
</script>
<style scoped>
p {
  margin-bottom: 0;
}

.hover:hover {
  opacity: 0.75;
  transition: 150ms;
}
</style>
