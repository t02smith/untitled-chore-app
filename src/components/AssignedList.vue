<script setup>
// API call to fetch user list
// store the response in a list (e.g. const users = ref(response.data))
// POST ... chores list
// wld use vue's v-for loop

import { ref } from 'vue';

const currUser = ref("")
const currChores = {
    one: ref(''),
    two: ref('')
}

function setCurrUser(name) {
    // chores.get(name) <- for when API works -- assuming chore list stored in 'const chores'
    currUser.value = name
    currChores.one.value = 'Hoover'
    currChores.two.value = 'Dishes'
}
</script>

<template>
    <h1 class="display-6">User's Chores</h1>
    <ul class="list-group">
        <li class="list-group-item">Tom<button @click="setCurrUser('Tom')" type="button" class="btn btn-dark btn-sml"
                data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/arrow.png"
                    alt="Image can't be displayed" width="20" height="20"></button> </li>
        <li class="list-group-item">Chris<button @click="setCurrUser('Chris')" type="button" class="btn btn-dark btn-sml"
                data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/arrow.png"
                    alt="Image can't be displayed" width="20" height="20"></button> </li>
    </ul>

    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ currUser }}'s Chores</h5>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <ul v-for="chore in currChores">
                        {{ chore }}
                    </ul>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
div.modal-body,
h5 {
    color: black;
}
</style>