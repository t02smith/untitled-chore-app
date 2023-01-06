<script setup>
</script>

<template>
  <nav class="navbar navbar-expand-lg navbar-dark fixed-top">
    <div class="container-fluid">
      <a class="navbar-brand">Untitled</a>
      <img src="@/assets/logo.png" alt="Image can't be displayed" width="40" height="40">

      <div class="collapse navbar-collapse" id="navbarNavAltMarkup">
        <ul class="navbar-nav me-auto">
        <li class="nav-item dropdown">
          <a class="nav-link dropdown-toggle" href="#" role="button" data-bs-toggle="dropdown" aria-expanded="false">
            Home
          </a>
          <ul class="dropdown-menu dropdown-menu-dark">
            <li><router-link to="/home/create" class="dropdown-item">Create</router-link></li>
            <li><router-link to="/home/dashboard" class="dropdown-item">Dashboard</router-link></li>
          </ul>
        </li>
        <li class="nav-item">
          <router-link to="/chores" class="nav-link">Chores</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/help" class="nav-link">Help</router-link>
        </li>
      </ul>
      <router-link to="/user" class="nav-link"><img src="@/assets/userIcon.png" alt="Image can't be displayed"
          width="40" height="40"></router-link>
      </div>
      </div>
  </nav>
</template>

<style scoped>
.router-link-exact-active {
  /* border-bottom: 2px solid white; */
  color: white;
}

li.nav-item {
  margin-left: 1em;
}

img {
  margin-right: 0.5em;
  float: right;
}
</style>