<script setup></script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark">
    <div class="container-fluid">
      <router-link
        to="/"
        class="d-flex flex-row align-items-center justify-content-center"
        style="text-decoration: none">
        <img src="@/assets/logo.svg" alt="Image can't be displayed" width="40" height="40" />

        <h5 class="navbar-brand font-bebas">Untitled Chore App</h5>
      </router-link>

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <div class="navbar-nav">
          <router-link to="/home/dashboard" class="nav-link" tag="link">Home</router-link>
          <router-link to="/chores" class="nav-link" tag="link">Chores</router-link>
          <router-link to="/help" class="nav-link" tag="link">Help</router-link>
        </div>
      </div>

      <router-link to="/user" class="nav-link"
        ><img src="@/assets/userIcon.png" alt="Image can't be displayed" width="40" height="40"
      /></router-link>
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
  left: 25%;
}

div.navbar-nav :link {
  margin-left: 6em;
}

img {
  margin-right: 0.5em;
}

h5 {
  margin: 0;
}
</style>
