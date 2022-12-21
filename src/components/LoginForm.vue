<script setup>
</script>

<template>
    <form>
        <img src="@/assets/logo.png" alt="Image can't be displayed" width="80" height="auto">

        <h1 class="display-6"> Sign in</h1>

        <div class="form-floating mb-3">
            <input type="text" class="form-control" id="username" placeholder="tc3g20">
            <label for="username" class="form-label">Username</label>
        </div>

        <div class="form-floating mb-3">
            <input type="password" class="form-control" id="passwd" placeholder="password101">
            <label for="passwd" class="form-label">Password</label>
            <div id="accntHelp" class="form-text">Don't have an account? Register</div>
        </div>

        <button type="submit" class="btn btn-primary">Log in</button>
    </form>
</template>

<style scoped>
form {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  color: black;
}

div.form-text {
    color: white;
}

h1 {
    margin-top: 0.5em;
    margin-bottom: 1em;
    color: white;
    font-size: 32px;
}
</style>