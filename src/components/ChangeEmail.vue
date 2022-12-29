<script setup>
// TODO state logic
</script>

<template>
    <div class="changeEmail">
        
        <h1 class="display-6">Change Email</h1>
        <div class="mb-3">
            <label for="formGroupExampleInput2" class="form-label">New Email</label>
            <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="New Email">
        </div>
        <div class="mb-3">
            <label for="formGroupExampleInput2" class="form-label">Current Password</label>
            <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Current Password">
        </div>
        <button type="button" class="btn btn-primary"
        style="--bs-btn-padding-y: .25rem; --bs-btn-padding-x: .5rem; --bs-btn-font-size: .99rem;">
        Save
        </button>
    </div>
    
</template>

<style scoped>

    div.changeEmail {
        left: 100%;
        top: 50%;
    }

</style>