<template>
  <div class="container p-4">
    <div class="jumbotron bg-dark p-4 my-4 shadow rounded">
      <h1 class="display-2 text-primary font-weight-bold">{{ props.title }}</h1>
      <p class="lead" v-if="!inviteLink">Generating the invite details for your new home...</p>

      <div class="lead" v-else>
        <p>
          House creator: <strong class="text-success"> {{ props.creator }} </strong>
          <br />
          House name: <strong class="text-success">{{ props.homeName }}</strong>
        </p>

        <p>
          Invite id: <strong class="text-success">{{ inviteLink.id }}</strong>
          <br />
          <i class="text-muted text-sm"
            >expires on <strong class="text-success"> {{ inviteLink.expiry }}</strong></i
          >
        </p>
      </div>

      <router-link
        v-if="props.showLink"
        class="btn btn-success"
        :to="`/home/dashboard?home=${props.creator}/${props.homeName}`"
        >Dashboard</router-link
      >
    </div>
  </div>
</template>
<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useHomeStore } from "../../stores/home";
import { useUserStore } from "../../stores/user";

const props = defineProps({
  creator: {
    type: String,
    required: true,
  },
  homeName: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: "Your Home's Invite Info",
  },
  showLink: {
    type: Boolean,
    default: false,
  },
});

const inviteLink = ref(null);
const user = useUserStore();
const home = useHomeStore();

onMounted(async () => {
  if (user.accessToken === null) return;
  inviteLink.value = await home.createInviteLink(props.creator, props.homeName);
});

watch(
  computed(() => `${props.creator}/${props.homeName}`),
  async () => {
    if (user.accessToken === null) return;
    inviteLink.value = await home.createInviteLink(props.creator, props.homeName);
  }
);
</script>
