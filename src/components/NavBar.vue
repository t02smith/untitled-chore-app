<template>
  <nav class="navbar navbar-dark bg-dark navbar-expand-lg py-2 px-3">
    <a href="#" class="navbar-brand d-flex gap-2 align-items-center">
      <img src="../assets/logo.png" alt="" width="40" height="40" />
      <strong>Untitled Chore App</strong>
    </a>
    <div
      class="collapse navbar-collapse justify-content-end d-flex align-items-center gap-2"
    >
      <ul class="navbar-nav">
        <li class="nav-item" v-for="link in ['homes', 'chores', 'timetable']">
          <a :href="`/${link}`" class="nav-link">{{ link }}</a>
        </li>
      </ul>
      <a href="/profile">
        <img
          src="../assets/logo.png"
          alt=""
          class="rounded-circle"
          width="35"
          height="35"
        />
      </a>
    </div>
  </nav>
</template>
