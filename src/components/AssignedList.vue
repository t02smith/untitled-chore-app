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

const delChore = ref('')

function setCurrUser(name) {
    // chores.get(name) <- for when API works -- assuming chore list stored in 'const chores'
    currUser.value = name
    currChores.one.value = 'Hoover ' + name
    currChores.two.value = 'Dishes ' + name

}

function deleteChore(chore) {
    delChore.value = chore
}
</script>

<template>
    <div class="modal fade" id="deleteChore" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Are you sure you want to delete this chore?</h5>
                    <button type="button" class="btn btn-success">Yes</button>
                    <button type="button" class="btn btn-danger">No</button>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    <ul>
                        {{ delChore }}
                    </ul>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <div class="modal fade" id="addChore" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">Adding chore to {{ currUser }}</h5>
                    <button type="button" class="btn btn-success">Add</button>
                    <button type="button" class="btn btn-danger" data-bs-dismiss="modal" aria-label="Close">Cancel</button>
                </div>
                <div class="modal-body">
                    <input v-model="uname" type="text" class="form-control" id="username" placeholder="Put the dishwasher on the fridge">
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Close</button>
                </div>
            </div>
        </div>
    </div>

    <div class="accordion" id="housemates">
        <h1 class="display-6">Housemates</h1>
        <div class="accordion-item">
            <h2 class="accordion-header" id="headingOne">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseOne" aria-expanded="true" aria-controls="collapseOne"
                @click="setCurrUser('Tom')">Tom<button type="button" id="addBut" class="btn btn-light btn-sml" data-bs-toggle="modal" data-bs-target="#addChore"><img src="@/assets/add.png" alt="Image can't be displayed" width="15"
                        height="15"></button>
                </button>
            </h2>
            <div id="collapseOne" class="accordion-collapse collapse show" aria-labelledby="headingOne" data-bs-parent="#housemates">
                <div class="accordion-body">
                    <li id="choresList" v-for="chore in currChores">
                        {{ chore }} <button type="button" id="binButton" class="btn btn-light btn-sml" data-bs-toggle="modal" data-bs-target="#deleteChore" @click=deleteChore(chore)><img src="@/assets/bin.png" alt="Image can't be displayed" width="11"
                        height="11"></button>
                    </li>
                </div>
            </div>
        </div>
        <div class="accordion-item">
            <h2 class="accordion-header" id="headingTwo">
                <button class="accordion-button collapsed" type="button" data-bs-toggle="collapse" data-bs-target="#collapseTwo" aria-expanded="false" aria-controls="collapseTwo"
                @click="setCurrUser('Chris')">
                    Chris<button type="button" class="btn btn-light btn-sml" data-bs-toggle="modal" data-bs-target="#addChore" id="addBut"><img src="@/assets/add.png" alt="Image can't be displayed" width="15"
                        height="15"></button>
                </button>
            </h2>
            <div id="collapseTwo" class="accordion-collapse collapse" aria-labelledby="headingTwo" data-bs-parent="#housemates">
                <div class="accordion-body">
                    <li v-for="chore in currChores">
                        {{ chore }} <button type="button" id="binButton" class="btn btn-light btn-sml" data-bs-toggle="modal" data-bs-target="#deleteChore" @click=deleteChore(chore)><img src="@/assets/bin.png" alt="Image can't be displayed" width="11"
                        height="11"></button>
                    </li>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
h1.display-6 {
    left: 30%;
    color: white;
    font-size: 32px;
}

div.modal-body,
h5 {
    color: black;
}

#housemates {
    left: 110%;
    width: 400px;
}

li.list-group-item {
    text-align: center;
}

li.list-group-item:hover {
    background-color: grey;
}


button.btn-light {
    border-radius: 24px;
}

#chores {
    left: 350%;
    bottom: 145px;
}

#binButton {
    background-color: red;
}

#addBut {
    margin-left: 7px;
}

</style>