<template>
  <div class="blog_info">
    <div class="blog_info_title">博文详情</div>
    <div class="user_info">
      <div
        class="user_head"
        :style="{ backgroundImage: 'url(' + blog_info.user_head + ')' }"
      ></div>
      <div class="other_info">
        <div class="user_name">
          {{ blog_info.user_name }}(@{{ blog_info.user_name }})
        </div>
        <div class="blog_time">{{ blog_info.created_at }}</div>
      </div>
    </div>
    <div class="blog_content">
      <span v-if="!show_detail">{{ weibo_content }}...</span>
      <span v-if="show_detail">{{ weibo_content_total }}</span>
      <div
        v-if="!show_detail"
        class="blog_info_show_detail"
        @click="showDetail"
      >
        详情
      </div>
      <div v-if="show_detail" class="blog_info_show_detail" @click="hideDetail">
        收起
      </div>
      <span v-html="'&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'"></span>
      <span v-for="topic in blog_info.topics" :key="topic.index"
        >#{{ topic }}#</span
      >
    </div>
    <div class="follow_info">转发()点赞()评论()</div>
  </div>
</template>

<script>
export default {
  name: "blog_info",
  data() {
    return {
      blog_info: {},
      show_detail: true,
      weibo_content: "",
      weibo_content_total: "",
    };
  },
  filters: {
    snippet(value) {
      if (value.length > 150) value = value.slice(0, 150) + "...";
      return value;
    },
  },
  methods: {
    getBlogInfo() {
      let query = this.$route.query;
      this.$axios
        .get("comment/post_detail?tag_task_id="+query.tag_task_id+"&weibo_id="+query.weibo_id)
        .then((res) => {
          this.blog_info = res;
          console.log(this.blog_info);
          this.blog_info.user_head = res.data.data.original_pics[0];
          this.weibo_content = res.data.data.weibo_content.slice(0, 150);
          this.weibo_content_total = res.data.data.weibo_content;
          if (this.weibo_content_total != this.weibo_content) {
            this.show_detail = false;
          }
        });
    },
    showDetail() {
      this.show_detail = true;
    },
    hideDetail() {
      this.show_detail = false;
    },
  },
  mounted() {
    this.getBlogInfo();
  },
};
</script>

<style scoped>
.blog_info {
  top: 1%;
  position: absolute;
  height: 35%;
  margin-left: 5px;
  width: 100%;
  background-color: #fff;
}
.blog_info_title {
  margin: 10px 20px;
  padding: 5px;
  font-weight: 600;
  letter-spacing: 1px;
}
.user_info {
  margin-left: 20px;
}
.user_head {
  width: 30px;
  height: 30px;
  background-size: cover;
}
.other_info {
  display: inline-block;
  margin-left: 20px;
}
.blog_time {
  color: #aaa;
}
.blog_content {
  font-size: 14px;
  margin: 5px 20px;
}
.follow_info {
  margin: 10px 20px;
  font-size: 13px;
  color: #aaa;
  padding-bottom: 10px;
}
.blog_info_show_detail {
  display: inline-block;
  color: skyblue;
  cursor: default;
}
.blog_info_show_detail:hover {
  font-weight: 600;
}
</style>