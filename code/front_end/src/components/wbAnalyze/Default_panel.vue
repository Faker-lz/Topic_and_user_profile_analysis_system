<template>
  <div class="default_panel">
    <div class="refresh" @click="refresh">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-shuaxin"></use>
      </svg>
    </div>
    <div class="default_panel_top">
      <span>
        <svg class="icon" aria-hidden="true">
          <use xlink:href="#icon-fx"></use>
        </svg>
      </span>
      <span class="title_text"> 舆情分析 </span>
    </div>
    <div v-if="topics_show" class="topics">
      <div
        class="topic"
        v-for="(defaultInfo, index) in defaultInfos"
        :key="defaultInfo.tag_task_id"
        @click="checkDetail(index)"
      >
        <div class="line"></div>
        <div class="delete" @click.stop="deleteTopic(defaultInfo.tag_task_id,index)"><i class="el-icon-close"></i></div>
        <div class="topic_name">话题:{{ defaultInfo.tag }}</div>
        <div class="other_info" v-if="!defaultInfo.status">
          用户数量:{{ defaultInfo.user_count }} 博文数量:{{
            defaultInfo.weibo_count
          }}
        </div>
        <div class="analyze" v-if="defaultInfo.status">
          <div class="loader">
            <span class="loader_top"></span>
            <span class="loader_bottom"></span>
          </div>
          <div class="loader_text">分析中，请稍后刷新...</div>
        </div>
        <div class="user_info" v-if="!defaultInfo.status">
          <div
            class="head"
            :style="{ backgroundImage: 'url(' + defaultInfo.head + ')' }"
          ></div>
          <div class="user">
            <div class="user_name">{{ defaultInfo.nickname }}</div>
            <div class="user_birthday">
              {{ defaultInfo.birthday }} --(weibo)
            </div>
          </div>
        </div>
        <!-- <div class="line"></div> -->
      </div>
    </div>
    <div v-if="!topics_show" class="topic_wait">
      <div class="box">
        <div class="circle"></div>
        <div class="circle"></div>
      </div>
      <h2>Loading...</h2>
    </div>
  </div>
</template>

<script>
export default {
  name: "default_panel",
  data() {
    return {
      defaultInfos: [],
      topics_show: "false",
    };
  },
  methods: {
    requesrInfo() {
      this.$axios.get("/tag_list").then((res) => {
        this.topics_show = true;
        this.defaultInfos = res.data.data;
        for (let index in this.defaultInfos) {
          this.defaultInfos[index] = {
            ...this.defaultInfos[index].vital_user,
            ...this.defaultInfos[index],
          };
        }
        this.$bus.$emit("send_tag_task_id", this.defaultInfos[0].tag_task_id);
      });
    },
    refresh() {
      this.topics_show = false;
      setTimeout(() => {
        this.requesrInfo();
      }, 2000);
    },
    checkDetail(index) {
      if (!this.defaultInfos[index].status) {
        this.$bus.$emit(
          "send_tag_task_id",
          this.defaultInfos[index].tag_task_id
        );
      } else {
        this.$message({
          message: "warning:该话题正在分析中...",
          type: "warning",
        });
      }
    },
    deleteTopic(id,index){
      this.$confirm('此操作将删除该话题, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$axios.get('delete_task?tag_task_id=' + id).then((res) =>{
          if(res.data.code == 0){
            this.defaultInfos.splice(index,1)
            this.$message({
              type: 'success',
              message: '删除成功!'
            });
          }else{
            this.$message({
              type: 'error',
              message: res.data.data
            });
          }
        });
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    }
  },
  mounted() {
    this.requesrInfo();
  },
};
</script>

<style scpoed>
.default_panel {
  height: 100%;
  width: 100%;
  background-color: #fff;
}
.default_panel_top {
  padding-top: 10px;
  height: 50px;
  text-align: center;
  font-size: 20px;
}
.topics {
  padding: 0 5px;
  height: 90%;
  overflow: auto;
}
.topics::-webkit-scrollbar {
  display: none;
}
.topic:hover {
  background: #ccc;
  -webkit-box-shadow: #ccc 0px 10px 10px;
  -moz-box-shadow: #ccc 0px 10px 10px;
  box-shadow: #ccc 0px 10px 10px;
  cursor: pointer;
}
.topic {
  height: 90px;
}
.line {
  margin-top: 4px;
  background-color: #eee;
  border: 1px solid #eee;
  width: 110%;
}
.head {
  width: 40px;
  height: 40px;
  background-size: 40px 40px;
  border-radius: 50%;
  margin-right: 10px;
}
.user_info {
  display: flex;
  margin-left: 10px;
}
.user_name {
  color: #6e6edb;
  font-size: 14px;
}
.user_birthday {
  font-size: 12px;
  color: #aaa;
}
.topic_name {
  margin-left: 35px;
  text-align: center;
  font-weight: 600;
  letter-spacing: 1px;
}
.delete {
  display: inline-block;
  font-size: 20px;
  height: 20px;
  color: #000;
  float: right;
}
.delete:hover{
  color: red;
  font-size: 25px;
}
.other_info {
  font-size: 12px;
  margin-bottom: 5px;
  text-align: center;
}
.icon {
  width: 30px;
  height: 30px;
}
.refresh {
  float: right;
}
.refresh .icon {
  width: 20px;
  height: 20px;
}
.loader {
  margin-left: 20px;
  width: 20px;
  height: 49px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  align-items: center;
  animation: roating 2s linear infinite;
}
@keyframes roating {
  0%,
  90% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(180deg);
  }
}
.loader::after {
  content: "";
  position: absolute;
  width: 1px;
  height: 24px;
  background-color: deepskyblue;
  top: 5px;
  animation: flow 2s linear infinite;
}
@keyframes flow {
  10%,
  100% {
    transform: translateY(16px);
  }
}
.loader_top,
.loader_bottom {
  width: 17px;
  height: 17px;
  border-style: solid;
  border-color: saddlebrown;
  border-width: 1px 1px 3px 3px;
  border-radius: 50% 100% 50% 30%;
  position: relative;
  overflow: hidden;
}
.loader_top {
  transform: rotate(-45deg);
}
.loader_bottom {
  transform: rotate(135deg);
}
.loader_top::before,
.loader_bottom::before {
  content: "";
  position: absolute;
  width: inherit;
  height: inherit;
  background-color: deepskyblue;
  animation: 2s linear infinite;
}
.loader_top::before {
  border-radius: 0 100% 0 0;
  animation-name: drop-sand;
}
@keyframes drop-sand {
  to {
    transform: translate(-12px, 12px);
  }
}
.loader_bottom::before {
  border-radius: 0 0 0 35%;
  animation-name: fill-sand;
  transform: translate(12px, -12px);
}
@keyframes fill-sand {
  to {
    transform: translate(0, 0);
  }
}
.loader_text {
  margin-left: 20px;
  margin-top: 15px;
  background: linear-gradient(to right, #39ec22, #099cb6);
  background-clip: text;
  -webkit-background-clip: text;
  color: transparent;
}
.analyze {
  display: flex;
}
.topic_wait {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-direction: column;
}
.topic_wait .box {
  position: relative;
  width: 50px;
  height: 50px;
  animation: rotatBox 10s linear infinite;
}
@keyframes rotatBox {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
.topic_wait .box .circle {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #38c1ff;
  border-radius: 50%;
  animation: animate 5s linear infinite;
}
.topic_wait .box .circle:nth-child(2) {
  background: #ff3378;
  animation-delay: -2.5s;
}
@keyframes animate {
  0% {
    transform: scale(1);
    transform-origin: left;
  }
  50% {
    transform: scale(0);
    transform-origin: left;
  }
  50.01% {
    transform: scale(0);
    transform-origin: right;
  }
  100% {
    transform: scale(1);
    transform-origin: right;
  }
}
.topic_wait h2 {
  margin-top: 20px;
  font-size: 20px;
  font-weight: 400;
  letter-spacing: 4px;
  color: #000;
}
</style>