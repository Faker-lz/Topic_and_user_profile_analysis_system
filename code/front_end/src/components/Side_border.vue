<template>
  <div class="side">
    <div class="side_background"></div>
    <div class="logo" @click="ToHome"></div>
    <div class="wb" @click="ToWB">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-weibo-copy"></use>
      </svg>
    </div>
    <div class="user">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-yonghu"></use>
      </svg>
    </div>
  </div>
</template>

<script>
export default {
  name: "side_border",
  methods: {
    ToWB() {
      this.$router.push({
        path: "/wb",
      });
    },
    ToHome() {
      this.$router.push({
        path: "/home",
      });
    },
  },
};
</script>

<style scoped>
.side {
  width: 100%;
  height: 100%;
}
.side_background {
  background: #2f323a;
  width: 100%;
  height: 100%;
}
.logo {
  position: relative;
  top: -100vh;
  width: 50px;
  height: 50px;
  background: #418de6 url("../assets/img/logo.png") no-repeat center center/40px;
}
.wb {
  position: relative;
  top: -100vh;
}
.user{
  position: relative;
  bottom: 22vh;
}
.icon {
  width: 50px;
  height: 50px;
}
</style>