<script setup>
import { ref, computed } from 'vue'

const mssg = ref("")

function sendMssg() {
    // Make POST req. to API with mssg as param.
}
</script>

<template>
    <div class="form">
        <h1 class="display-6">Contact Us</h1>
        <div class="form-floating">
            <textarea v-model="mssg" class="form-control" placeholder="Leave a comment here" id="floatingTextarea2"
                style="height: 100px"></textarea>
            <label for="floatingTextarea2">Message</label>
        </div>
        <button @click="sendMssg()" class="btn btn-primary">Send</button>
    </div>
</template>

<style scoped>
div.form {
    color: black;
    left: 250%;
    text-align: center;
    padding: 2em;
}

button {
    margin-top: 1em;
    float: right;
}

h1 {
    margin-bottom: 0.5em;
    color: white;
    font-size: 32px;
}
</style>
