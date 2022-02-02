<template>
  <div class="hot_point">
    <div class="hot_point_title">热点转发</div>
    <div class="hot_point_contents">
      <div
        class="hot_point_content"
        v-for="(comment, index) in comments"
        :key="index"
      >
        <div class="hot_point_number red" v-if="index == 0">
          {{ index + 1 }}
        </div>
        <div class="hot_point_number orange" v-if="index == 1">
          {{ index + 1 }}
        </div>
        <div class="hot_point_number blue" v-if="index == 2">
          {{ index + 1 }}
        </div>
        <div class="hot_point_number" v-if="index >= 3">{{ index + 1 }}</div>
        <span>{{ comment.content | snippet }}</span>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "hot_point",
  data() {
    return {
      comments: [],
    };
  },
  filters: {
    snippet(value) {
      if (value.length > 25) value = value.slice(0, 25) + "...";
      return value;
    },
  },
  methods: {
    getHotPoint() {
      let query = this.$route.query;
      this.$axios
        .get("comment/key_node?tag_task_id="+query.tag_task_id+"&weibo_id="+query.weibo_id)
        .then((res) => {
          console.log(res)
          this.comments = res.data.comments;
        });
    },
  },
  mounted() {
    this.getHotPoint();
  },
};
</script>

<style scoped>
.hot_point {
  position: absolute;
  width: 100%;
  height: 54%;
  top: 46%;
  background-color: #fff;
}
.hot_point_title {
  margin: 10px 20px;
  padding: 5px;
  font-weight: 600;
  letter-spacing: 1px;
}
.hot_point_content {
  margin-left: 20px;
  padding: 5px;
  font-size: 14px;
}
.hot_point_number {
  display: inline-block;
  width: 20px;
  height: 20px;
  text-align: center;
  background-color: #ccc;
  color: #fff;
  margin-right: 10px;
}
.red {
  background-color: rgb(255, 0, 0);
}
.orange {
  background-color: rgb(255, 115, 0);
}
.blue {
  background-color: rgb(0, 183, 249);
}
</style>