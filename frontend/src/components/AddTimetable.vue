<script setup>
// TODO state logic
</script>

<template>
    <div class="addTimetable">
        <h1 class="display-6">Add Timetable</h1>
        <!-- Temporary template, change when decide how to handle timetables -->
        <div class="d-grid gap-3 col-7">
            <button class="btn btn-primary" type="button">Import</button>
            <button class="btn btn-primary" type="button">Delete</button>
        </div>    
    </div>
</template>

<style scoped>
    .addTimetable {
        min-width: 500px;
        min-height: 500px;
        padding-top: 50px; 
    }

    .display-6 {
        color: white;
        margin-bottom: 40px;
    }

    .btn {
        width: 100px;
    }
</style>