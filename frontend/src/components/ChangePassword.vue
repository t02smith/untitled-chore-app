<script setup>
// TODO state logic
</script>

<template>
    <div class="changePassword">
        <h1 class="display-6">Change Password</h1>
        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="currentPassword" placeholder="Current Password">
            <label for="currentPassword">Current Password</label>
        </div>
        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="password" placeholder="New Password">
            <label for="password">New Password</label>
        </div>
        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="password" placeholder="Confirm New Password">
            <label for="password">Confirm New Password</label>
        </div>
        <button type="button" class="btn btn-primary">
        Save
        </button>
    </div>
</template>

<style scoped>
    .changePassword {
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