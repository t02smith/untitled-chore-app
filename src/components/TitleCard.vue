<template>
  <div class="title-card font-bebas text-left gap-2 flex-row-reverse align-items-center">
    <h1 class="text-white" style="line-height: 80%">
      Untitled <br />
      Chore <br />
      App
    </h1>

    <img src="../assets/logo.svg" alt="" width="140" height="140" />
  </div>
</template>
<style scoped>
div {
  display: flex;
}

div > h1 {
  font-size: 3rem;
}

@media (min-width: 768px) {
  div > img {
    width: 325px;
    height: 325px;
  }

  div > h1 {
    font-size: 8rem;
  }
}
</style>
