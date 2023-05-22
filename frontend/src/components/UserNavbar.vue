<script setup>
    import ChangeEmail from "../components/ChangeEmail.vue";
    import ChangePassword from "../components/ChangePassword.vue";
    import DeleteAccount from "../components/DeleteAccount.vue";
    import AddTimetable from "../components/AddTimetable.vue";
</script>

<template>
    <div class="d-flex align-items-center userNav">
        <div class="nav flex-column nav-pills me-3 " id="v-pills-tab" role="tablist" aria-orientation="vertical">
            <p class="display-6 navHeader">User Settings</p>
            <button class="nav-link active" id="v-pills-addTimetable-tab" data-bs-toggle="pill" data-bs-target="#v-pills-addTimetable" type="button" role="tab" aria-controls="v-pills-addTimetable" aria-selected="false">Add Timetable</button>
            <button class="nav-link" id="v-pills-changePassword-tab" data-bs-toggle="pill" data-bs-target="#v-pills-changePassword" type="button" role="tab" aria-controls="v-pills-changePassword" aria-selected="false">Change Password</button>
            <button class="nav-link" id="v-pills-changeEmail-tab" data-bs-toggle="pill" data-bs-target="#v-pills-changeEmail" type="button" role="tab" aria-controls="v-pills-changeEmail" aria-selected="true">Change Email</button>
            <button class="nav-link" id="v-pills-deleteAccount-tab" data-bs-toggle="pill" data-bs-target="#v-pills-deleteAccount" type="button" role="tab" aria-controls="v-pills-deleteAccount" aria-selected="false">Delete Account</button>     
        </div>
        <div class="tab-content" id="v-pills-tabContent">
            <div class="tab-pane fade show active" id="v-pills-addTimetable" role="tabpanel" aria-labelledby="v-pills-addTimetable-tab" tabindex="0"><AddTimetable /></div>
            <div class="tab-pane fade" id="v-pills-changePassword" role="tabpanel" aria-labelledby="v-pills-changePassword-tab" tabindex="0"><ChangePassword /></div>
            <div class="tab-pane fade" id="v-pills-changeEmail" role="tabpanel" aria-labelledby="v-pills-changeEmail-tab" tabindex="0"><ChangeEmail /></div>
            <div class="tab-pane fade" id="v-pills-deleteAccount" role="tabpanel" aria-labelledby="v-pills-deleteAccount-tab" tabindex="0"><DeleteAccount /></div>
        </div>
    </div>
</template>

<style scoped>
.userNav {
    left: 20%;
    gap: 250px;
}

.navHeader {
    color: white;
    font-size: 30px;
    padding-left: 5px;
}

.nav-link {
    font-size: 16px;
    color: rgb(209, 209, 209);
}
</style>