<template>
  <div class="card text-white bg-dark shadow">
    <div class="card-body">
      <div class="d-flex gap-3 align-items-center">
        <font-awesome-icon :icon="props.icon" :style="`color: ${props.color}`" style="font-size: 2rem" />
        <div class="flex-grow-1">
          <h5 class="card-title">
            {{ `${props.name} ${props.username && `• ${props.username}`}` }}
          </h5>
          <h6 class="card-subtitle" style="margin-top: -0.5rem" :style="`color: ${props.color};`">
            {{ props.room }}
          </h6>
          <b v-if="props.expectedTime && props.difficulty" class="text-muted">
            {{ difficultyToSymbol() }} • <font-awesome-icon icon="fa-solid fa-stopwatch" /> {{ props.expectedTime }}
          </b>
        </div>

        <slot />
      </div>
    </div>
  </div>
</template>
<script setup>
const props = defineProps({
  name: {
    type: String,
    required: true,
  },
  room: {
    type: String,
    required: true,
  },
  username: {
    type: String,
    default: "",
  },
  color: {
    type: String,
    default: "#fff",
  },
  icon: {
    type: String,
    required: "fa-solid fa-house",
  },
  expectedTime: {
    type: Number,
    default: null,
  },
  difficulty: {
    type: Number,
    default: null,
  },
});

function difficultyToSymbol() {
  switch (props.difficulty) {
    case 1:
      return "⬜";
    case 2:
      return "🟩";
    case 3:
      return "🟦";
    case 4:
      return "🟪";
    case 5:
      return "🟧";
  }
}
</script>
