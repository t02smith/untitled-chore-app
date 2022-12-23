<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDetails } from "@/stores/userDetails"

const router = useRouter();
const uname = ref("")
const pwd = ref("")

function login() {
    // send off to API:
        // POST req. to URL of azure func. "https://blah"
        // uname.value
        // pwd.value
        // console.log('[LOGIN] ' + uname.value + ' logged in')

    // store in pinia
    const detailsStore = useDetails() // access pinia through the instance
    detailsStore.setDetails(uname.value, pwd.value);
    
    // TO REMOVE
    console.log('[LOGIN] Username: ' + uname.value);
    router.push({ path: '/home' });
}
</script>

<template>
    <div class="form">
        <img src="@/assets/logo.png" alt="Image can't be displayed" width="85" height="85">

        <h1 class="display-6">Sign in</h1>

        <div class="form-floating mb-3">
            <input v-model="uname" type="text" class="form-control" id="username" placeholder="tc3g20">
            <label for="username" class="form-label">Username</label>
        </div>

        <div class="form-floating mb-3">
            <input v-model="pwd" type="password" class="form-control" id="passwd" placeholder="password101">
            <label for="passwd" class="form-label">Password</label>
            <div id="accntHelp" class="form-text">Don't have an account? <router-link to="/register">Register</router-link></div>
        </div>

        <button @click="login" class="btn btn-primary">Log in</button>
    </div>
</template>

<style scoped>
div.form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: black;
}

div.form-text {
    color: white;
}

h1 {
    margin-top: 0.5em;
    margin-bottom: 1em;
    color: white;
    font-size: 32px;
}
</style>