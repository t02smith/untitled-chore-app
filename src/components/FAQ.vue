<script setup>
import { ref } from 'vue'

const question = ref("")
const answer = ref("")

function setFaq(q, a) {
    question.value = q
    answer.value = a
}
</script>

<template>
    <div class="faq">
        <div class="list">
            <h1 class="display-6">FAQs</h1>
            <ul class="list-group">
                <li class="list-group-item">Can I be in more than 1 home? <button type="button"
                        class="btn btn-light btn-sml"
                        @click="setFaq('Can I be in more than 1 home?', 'Yes - to join a new home go to ')"
                        data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/add.png"
                            alt="Image can't be displayed" width="10" height="10"></button></li>
                <li class="list-group-item">How are chores assigned? <button type="button" class="btn btn-light btn-sml"
                        @click="setFaq('How are chores assigned?', 'Each home has an admin user who assigns chores. The schedule is determined based on your university timetable')"
                        data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/add.png"
                            alt="Image can't be displayed" width="10" height="10"></button></li>
                <li class="list-group-item">What if I am unable to do a chore? <button type="button"
                        class="btn btn-light btn-sml"
                        @click="setFaq('What if I am unable to do a chore?', 'Mark the chore as done and make the admin aware that it is incomplete. If you forget to mark as complete your chore score will be affected')"
                        data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/add.png"
                            alt="Image can't be displayed" width="10" height="10"></button></li>
                <li class="list-group-item">What does chore score mean? <button type="button"
                        class="btn btn-light btn-sml"
                        @click="setFaq('What does chore score mean?', 'It reflects how consistent you are at doing your chores, where a higher score means you are more consistent')"
                        data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/add.png"
                            alt="Image can't be displayed" width="10" height="10"></button></li>
                <li class="list-group-item">How do I know when to do chores? <button type="button"
                        class="btn btn-light btn-sml"
                        @click="setFaq('How do I know when to do chores?', 'Your TODO list is available on the home dashboard')"
                        data-bs-toggle="modal" data-bs-target="#exampleModal"><img src="@/assets/add.png"
                            alt="Image can't be displayed" width="10" height="10"></button></li>
            </ul>
        </div>

        <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">{{ question }}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">{{ answer }}</div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
img {
    top: -55%;
}

button.btn-light {
    margin-left: 0.5em;
    width: 20px;
    height: 20px;
    padding: 2.6px 3.6px;
    border-radius: 12px;
}

div.modal-body {
    color: black;
}

div.list {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    text-align: center;
}

h1 {
    margin-bottom: 0.5em;
    color: white;
    font-size: 32px;
}

h5 {
    color: black;
}

li {
    margin-bottom: 0.1em;
    color: white;
    font-size: 16px;
    background: #545353;
}
</style>