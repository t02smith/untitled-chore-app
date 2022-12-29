<script setup>
    import ChangeEmail from "../components/ChangeEmail.vue";
    import ChangePassword from "../components/ChangePassword.vue";
</script>

<template>
    <div class="d-flex align-items-start">
        <div class="nav flex-column nav-pills me-3" id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <button class="nav-link active" id="v-pills-changeEmail-tab" data-bs-toggle="pill" data-bs-target="#v-pills-changeEmail" type="button" role="tab" aria-controls="v-pills-changeEmail" aria-selected="true">Change Email</button>
            <button class="nav-link" id="v-pills-changePassword-tab" data-bs-toggle="pill" data-bs-target="#v-pills-changePassword" type="button" role="tab" aria-controls="v-pills-changePassword" aria-selected="false">Change Password</button>
            <button class="nav-link" id="v-pills-messages-tab" data-bs-toggle="pill" data-bs-target="#v-pills-messages" type="button" role="tab" aria-controls="v-pills-messages" aria-selected="false">Messages</button>
            <button class="nav-link" id="v-pills-settings-tab" data-bs-toggle="pill" data-bs-target="#v-pills-settings" type="button" role="tab" aria-controls="v-pills-settings" aria-selected="false">Settings</button>
        </div>
        <div class="tab-content" id="v-pills-tabContent">
            <div class="tab-pane fade show active" id="v-pills-changeEmail" role="tabpanel" aria-labelledby="v-pills-changeEmail-tab" tabindex="0"><ChangeEmail /></div>
            <div class="tab-pane fade" id="v-pills-changePassword" role="tabpanel" aria-labelledby="v-pills-changePassword-tab" tabindex="0"><ChangePassword /></div>
            <div class="tab-pane fade" id="v-pills-messages" role="tabpanel" aria-labelledby="v-pills-messages-tab" tabindex="0">...</div>
            <div class="tab-pane fade" id="v-pills-settings" role="tabpanel" aria-labelledby="v-pills-settings-tab" tabindex="0">...</div>
        </div>
    </div>
</template>

<style scoped>

</style>