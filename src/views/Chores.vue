<script setup>
import Navbar from "../components/Navbar.vue";
import AssignedList from "../components/AssignedList.vue";

function add() {
}

function del() {

}
</script>

<template>
    <main>
        <Navbar />
        <button @click="add" type="button" class="btn btn-success btn-lg">Add Chore</button>
        <button @click="del" type="button" class="btn btn-danger btn-lg">Delete Chore</button>
        <AssignedList />
    </main>
</template>

<style scoped>
</style>