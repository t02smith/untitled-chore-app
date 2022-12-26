<template>
  <div class="card text-white bg-dark shadow">
    <div class="card-body">
      <div class="d-flex gap-3 align-items-center">
        <font-awesome-icon
          :icon="props.icon"
          :style="`color: ${props.color}`"
          style="font-size: 2rem"
        />
        <div class="flex-grow-1">
          <h5 class="card-title">
            {{ `${props.name} ${props.username && `• ${props.username}`}` }}
          </h5>
          <h6
            class="card-subtitle"
            style="margin-top: -0.5rem"
            :style="`color: ${props.color};`"
          >
            {{ props.room }}
          </h6>
        </div>
        <input
          v-if="!props.noToggle"
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
  username: {
    type: String,
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
  noToggle: {
    type: Boolean,
    default: true,
  },
});
</script>
