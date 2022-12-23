<template>
  <div class="card text-white bg-dark shadow" style="width: 20rem">
    <div class="card-body">
      <div class="d-flex gap-3 align-items-center">
        <img :src="props.icon" alt="" class="rounded-full" />
        <div class="flex-grow-1">
          <h5 class="card-title">{{ props.name }}</h5>
          <h6
            class="card-subtitle"
            style="margin-top: -0.5rem"
            :style="`color: ${props.color};`"
          >
            {{ props.room }}
          </h6>
        </div>
        <input
          type="checkbox"
          name=""
          id=""
          class="form-check-input ms-2 bg-secondary justify-self-end"
          style="width: 2rem; height: 2rem"
          @click="onToggle"
        />
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
  color: {
    type: String,
    default: "#ccc",
  },
  icon: {
    type: String,
    required: true,
  },
  onToggle: {
    type: Function,
  },
});
</script>
