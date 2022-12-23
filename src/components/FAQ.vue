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
        <h1 class="display-6">FAQs</h1>
        <ul class="list-group">
            <li class="list-group-item">Why are my housemates dead? <button type="button" class="btn btn-light btn-sml"
                    @click="setFaq('Why are my housemates dead?', 'Skill issue')" data-bs-toggle="modal"
                    data-bs-target="#exampleModal"><img src="@/assets/add.png" alt="Image can't be displayed" width="10"
                        height="10"></button></li>
            <li class="list-group-item">Is this cw fun? <button type="button" class="btn btn-light btn-sml"
                    @click="setFaq('Is this cw fun?', 'It is pain')" data-bs-toggle="modal"
                    data-bs-target="#exampleModal"><img src="@/assets/add.png" alt="Image can't be displayed" width="10"
                        height="10"></button></li>
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


</template>

<style scoped>
img {
    top: -50%;
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

div.faq {
    left: -50%;
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
    margin-bottom: 0.5em;
    color: white;
    font-size: 16px;
    background: black;
}
</style>