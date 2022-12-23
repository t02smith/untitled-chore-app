<script setup>
</script>

<template>
    <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
        <div class="container-fluid">
            <a class="navbar-brand">Untitled</a>
            <img src="@/assets/logo.png" alt="Image can't be displayed" width="40" height="40">

            <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
                <div class="navbar-nav">
                    <router-link to="/home" class="nav-link" tag="link">Home</router-link>
                    <router-link to="/group" class="nav-link" tag="link">Group</router-link>
                    <router-link to="/chores" class="nav-link" tag="link">Chores</router-link>
                    <router-link to="/help" class="nav-link" tag="link">Help</router-link>
                </div>
            </div>

            <router-link to="/user" class="nav-link"><img src="@/assets/userIcon.png" alt="Image can't be displayed"
                    width="40" height="40"></router-link>
        </div>
    </nav>
</template>

<style scoped>
.router-link-exact-active {
    border-bottom: 2px solid white;
    color: white;
}

div.navbar-nav {
    /* This is extremely jank must change lol */
    /* Centering not working properly otherwise */
    left: 20%;
}

div.navbar-nav :link {
    margin-left: 6em;
}

img {
    margin-right: 0.5em;
}
</style>