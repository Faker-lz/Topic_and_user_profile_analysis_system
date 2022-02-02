<template>
  <div class="participation_list">
    <div class="participation_list_title">人员列表(按参与度排序)</div>
    <div class="participation_list_person_lists">
      <div
        class="participation_list_person_list"
        v-for="person in person_list"
        :key="person.index"
      >
        <div class="nf">
          <div class="person_head">
            <img :src="person.head" alt="" />
          </div>
          <div class="person_info">
            <div class="person_name">
              {{ person.nickname }}(@{{ person.nickname }})
            </div>
            <div class="person_time">{{ person.birthday }}</div>

          </div>
        </div>
        <div class="mark">
          <span class="marks" v-for="(mark, index) in person.marks" :key="index">
            {{mark.name}}
          </span>
        </div>
<!--        <div class="popover">-->
<!--          <el-popover-->
<!--            placement="right"-->
<!--            title="详情"-->
<!--            width="150"-->
<!--            trigger="click"-->
<!--            content="这是一段内容,这是一段内容,这是一段内容,这是一段内容。"-->
<!--          >-->
<!--            <el-button slot="reference">查看详情</el-button>-->
<!--          </el-popover>-->
<!--        </div>-->
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "participation_list",
  data() {
    return {
      person_list: [],
    };
  },
  methods: {
    getPersonList() {
      let query = this.$route.query;
      this.$axios.get("user_mark?tag_task_id=" + query.tag_task_id).then((res) => {
        console.log(res.data.data)
        this.person_list = res.data.data;
      });
    },
  },
  mounted() {
      this.getPersonList();
  },
};
</script>

<style scoped>
.participation_list_title {
  position: relative;
  margin: 10% auto;
  width: 25vw;
  font-size: 1.3rem;
  font-weight: 600;
  text-align: center;
}
.participation_list_person_lists {
  width: 25vw;
  height: 92vh;
  overflow: auto;
}
.participation_list_person_lists::-webkit-scrollbar {
  width: 10px;
  height: 1px;
}
.participation_list_person_lists::-webkit-scrollbar-thumb {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: #eee;
}
.participation_list_person_lists::-webkit-scrollbar-track {
  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);
  background: #fff;
}
.participation_list_person_list {
  height: 13vh;
  border-top: 1px solid #aaa;
}
.nf{
  display: flex;
}
.person_head img {
  margin: 20px 0 0 20px;
  height: 60px;
  width: 60px;
  border-radius: 50%;
}
.person_info {
  margin: 25px 0 0 20px;
  flex :1;
}
.person_name {
  margin-bottom: 5px;
  color: deepskyblue;
}
.person_time {
  color: #aaa;
  font-size: 0.5rem;
}
.mark{
  margin: 10px 0  0 10px;
  font-size: 18px;
  font-weight: 600;
  color: #62acfc;
}
</style>