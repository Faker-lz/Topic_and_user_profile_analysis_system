<template>
  <div class="home">
    <img src="../assets/img/school.jpg" alt="" />
    <div class="table">
      <div class="bg" @click="bgClick">
        <h1>{{ currentTime }}</h1>
        <p>{{ currentDate }}</p>
        <h5>designed&created by yuan</h5>
        <i class="fa fa-angle-down fa-3x" aria-hidden="true"></i>
        <i class="fa fa-angle-down fa-3x" aria-hidden="true"></i>
        <h6>点击向下滑动</h6>
      </div>

      <div class="up" @click="upClick">
        <i class="fa fa-angle-up fa-3x" aria-hidden="true"></i>
        <i class="fa fa-angle-up fa-3x" aria-hidden="true"></i>
      </div>
    </div>

    <div class="home_container">
      <div class="con">
        <div class="box">
          <div class="content" @click="ToWB">
            <svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-weibo"></use>
            </svg>
          </div>
          <div>微博舆论分析</div>
        </div>
        <div class="box">
          <div class="content">
            <a href="#">
              <img src="../assets/img/favicon.png" alt="" />
            </a>
          </div>
          <div>网络安全</div>
        </div>
        <div class="box">
          <div class="content">
            <a href="#">
              <img src="../assets/img/favicon.png" alt="" />
            </a>
          </div>
          <div>网络安全</div>
        </div>
        <div class="box">
          <div class="content" @click="ToLogin">
            <svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-denglu-copy"></use>
            </svg>
          </div>
          <div>登录</div>
        </div>
        <div class="box">
          <div class="content">
            <svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-denglu1-copy"></use>
            </svg>
          </div>
          <div>账号管理</div>
        </div>
        <div class="box">
          <div class="content">
            <svg class="icon" aria-hidden="true">
              <use xlink:href="#icon-denglurizhi-copy"></use>
            </svg>
          </div>
          <div>登录日志</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import $ from "jquery";
export default {
  name: "home",
  components: {},
  data() {
    return {
      flag: true,
      timer: "",
      currentDate: "",
      currentTime: "",
      title: ["早上好", "中午好", "下午好", "晚上好"],
      content: [
        "元气满满的一天!",
        "开始摸鱼!",
        "饮茶先啦!",
        "这个点还没下班的人一定还没下班吧?",
      ],
    };
  },
  methods: {
    bgClick() {
      if (this.flag) {
        $(".table").animate(
          {
            top: -100 + "vh",
          },
          500
        );
        $(".home>img").animate(
          {
            width: 120 + "%",
            height: 120 + "%",
            left: -10 + "%",
          },
          500
        );
        $(".home_container").animate(
          {
            top: -10 + "%",
          },
          500
        );
        this.flag = false;
      }
    },
    upClick() {
      if (!this.flag) {
        $(".table").animate(
          {
            top: 0,
          },
          500
        );
        $(".home>img").animate(
          {
            width: 100 + "%",
            height: 100 + "%",
            left: 0,
          },
          500
        );
        $(".home_container").animate(
          {
            top: 100 + "%",
          },
          500
        );
        this.flag = true;
      }
    },
    ToWB() {
      this.$router.push({
        path: "/wb",
      });
    },
    ToLogin() {
      this.$router.push({
        path: "/login",
      });
    },
  },
  mounted() {
    const h = this.$createElement;
    let t = 0;
    let hour = new Date().getHours();
    if (5 <= hour && hour <= 11) t = 0;
    else if (11 < hour && hour <= 14) t = 1;
    else if (14 < hour && hour <= 18) t = 2;
    else t = 3;
    this.$notify({
      title: this.title[t],
      message: h("i", { style: "color: teal" }, this.content[t]),
    });
  },
  created() {
    let date = new Date();
    this.currentDate =
      date.getFullYear() +
      "年" +
      (date.getMonth() + 1) +
      "月" +
      date.getDate() +
      "日";
    this.timer = setInterval(() => {
      let date = new Date();
      let hour = date.getHours();
      let minute = date.getMinutes();
      let second = date.getSeconds();
      hour = hour < 10 ? "0" + hour : hour;
      minute = minute < 10 ? "0" + minute : minute;
      second = second < 10 ? "0" + second : second;
      this.currentTime = hour + ":" + minute + ":" + second;
    }, 1000);
  },
  beforeDestroy() {
    if (this.timer) {
      clearInterval(this.timer);
    }
  },
};
</script>

<style scoped>
.home {
  width: 100%;
  height: 100vh;
  overflow: hidden;
  position: relative;
}
.home > img {
  width: 100vw;
  height: 100vh;
  position: absolute;
  transform: scale(1.6);
  animation: home 1s ease-out forwards;
}
.table {
  width: 100%;
  height: 20vh;
  position: relative;
}
.bg {
  position: relative;
  width: 100%;
  height: 100vh;
  user-select: none;
}
.bg h1 {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translateX(-50%);
  font-size: 100px;
  font-weight: 600;
  letter-spacing: 10px;
  color: #fff;
  z-index: 1;
  animation: bg_h1 0.5s ease-out forwards;
}
.bg p {
  margin-top: 80px;
  position: absolute;
  left: 50%;
  transform: translateX(-50%);
  font-size: 20px;
  letter-spacing: 10px;
  color: #fff;
  font-weight: 100;
  z-index: 1;
  animation: bg_p 0.5s ease-out forwards 0.3s;
}
.bg h5 {
  position: absolute;
  top: 1%;
  left: 50%;
  transform: translateX(-50%);
  letter-spacing: 10px;
  color: #fff;
  font-weight: 100;
  z-index: 1;
  opacity: 0;
  animation: bg_h5 0.3s ease-out forwards 0.6s;
}
.bg h6 {
  position: absolute;
  top: 90%;
  left: 50%;
  transform: translateX(-50%);
  letter-spacing: 5px;
  color: #fff;
  font-weight: 100;
  z-index: 1;
  opacity: 0;
  animation: bg_h6 0.3s ease-out forwards 0.6s;
}
.bg i:nth-child(4) {
  z-index: 1;
  color: #fff;
  position: absolute;
  bottom: 2vh;
  left: 50%;
  transform: translateX(-50%);
  animation: bg_i 1s infinite;
}
.bg i:nth-child(5) {
  z-index: 1;
  color: #fff;
  position: absolute;
  bottom: 0vh;
  left: 50%;
  transform: translateX(-50%);
  animation: bg_i 1s 0.5s infinite;
}

@keyframes bg_h1 {
  from {
    top: 70%;
    opacity: 0;
  }
  to {
    top: 30%;
    opacity: 1;
  }
}
@keyframes bg_p {
  from {
    top: 80%;
    opacity: 0;
  }
  to {
    top: 50%;
    opacity: 1;
  }
}
@keyframes bg_h5 {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
@keyframes bg_h6 {
  from {
    top: 100%;
    opacity: 0;
  }
  to {
    top: 80%;
    opacity: 1;
  }
}
@keyframes home {
  from {
    transform: scale(1.6);
  }
  to {
    transform: scale(1);
  }
}
@keyframes bg_i {
  0% {
    opacity: 1;
  }
  50% {
    opacity: 0;
  }
  100% {
    opacity: 1;
  }
}

.up i:nth-child(1) {
  z-index: 1;
  color: #fff;
  position: absolute;
  top: 100vh;
  left: 50%;
  transform: translateX(-50%);
  animation: bg_i 1s infinite;
}
.up i:nth-child(2) {
  z-index: 1;
  color: #fff;
  position: absolute;
  top: 102vh;
  left: 50%;
  transform: translateX(-50%);
  animation: bg_i 1s 0.5s infinite;
}
.home_container {
  position: relative;
  top: 100%;
  width: 100%;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  flex-wrap: wrap;
  color: #fff;
}
.home_container .con {
  width: 30%;
  height: 40%;
  border-radius: 20px;
  backdrop-filter: blur(30px);
  display: grid;
  grid-template-columns: 1fr 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  grid-gap: 20px;
  padding: 20px;
}
.home_container .box {
  display: flex;
  justify-content: space-between;
  flex-direction: column;
  align-items: center;
  padding: 1opx;
  border: 1px solid rgba(255, 255, 255, 0);
  transition: border 0.5s;
}
.home_container .box:hover {
  border: 1px solid rgba(255, 255, 255, 1);
  transition: border 0.5s;
}
.home_container .content {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  height: 100%;
}
.icon{
  width: 80px;
  height: 80px;
}
.home_container a img {
  width: 80px;
}
</style>