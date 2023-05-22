<script setup>
// TODO state logic
</script>

<template>
    <div class="deleteAccount">
        <h1 class="display-6">Delete Account</h1>

        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="currentPassword" placeholder="Current Password">
            <label for="currentPassword">Current Password</label>
        </div>

        <!-- Button trigger modal -->
        <button type="button" class="btn btn-primary" data-bs-toggle="modal" data-bs-target="#exampleModal">
        Delete Account
        </button>
    </div>
       <!-- Modal -->
    <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <div class="modal-header">
                    <h1 class="modal-title" id="exampleModalLabel">Warning!</h1>
                    <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                </div>
                <div class="modal-body">
                    Once you delete your account you can never get it back!
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cancel</button>
                    <button type="button" class="btn btn-primary delete">Delete</button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>
    div.deleteAccount {
        min-width: 500px;
        min-height: 500px;
        padding-top: 50px;
    }

    .display-6 {
        color: white;
        margin-bottom: 40px;
    }

    div.modal-body {
        color: black;
    }

    .modal-title {
        color:rgb(0, 0, 0);
        font-size: 32px;   
    }

    .mb-3 {
        color: black;
        width:250px;
    }

    .delete {
        background-color:rgb(227, 27, 27);  
    }
</style>