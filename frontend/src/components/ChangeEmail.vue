<script setup>
// TODO state logic
</script>

<template>
    <div class="changeEmail"> 
        <h1 class="display-6">Change Email</h1>
        <div class="form-floating mb-3">
            <input type="email" class="form-control" id="newEmail" placeholder="New Email">
            <label for="newEmail">New Email</label>
        </div>
        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="currentPassword" placeholder="Current Password">
            <label for="currentPassword">Current Password</label>
        </div>
        <button type="button" class="btn btn-primary">
        Save
        </button>
    </div>  
</template>

<style scoped>
    .changeEmail {
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

    .mb-3 {
        color: black;
        width:250px;
    }
</style>