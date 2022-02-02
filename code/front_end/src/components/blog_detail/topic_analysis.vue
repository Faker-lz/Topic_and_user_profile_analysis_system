<template>
  <div class="topic_analysis">
    <div class="topic_analysis_title">主题分析</div>
    <div id="topic_analysis_graph"></div>
  </div>
</template>

<script>
export default {
  name: "topic_analysis",
  data() {
    return {
      topic_analysis: [],
    };
  },
  methods: {
    myTopicAnalysis() {
      let myChart = this.$echarts.init(
        document.getElementById("topic_analysis_graph")
      );
      let option;
      let query = this.$route.query;
      this.$axios
        .get(
            "comment/cluster/type?tag_task_id="+query.tag_task_id+"&weibo_id="+query.weibo_id
        )
        .then((res) => {
          console.log(res)
          for (let index in res.data.data) {
            this.topic_analysis[index] = res.data.data[index];
            this.topic_analysis[index].name = res.data.data[index].key;
            this.topic_analysis[index].value = res.data.data[index].doc_count;
          }
          option = {
            legend: {
              orient: "vertical",
              right: "right",
            },
            tooltip: {
              trigger: "item",
            },
            series: [
              {
                name: "主题分析",
                type: "pie",
                radius: "50%",
                data: this.topic_analysis,
                emphasis: {
                  itemStyle: {
                    shadowBlur: 10,
                    shadowOffsetX: 0,
                    shadowColor: "rgba(0, 0, 0, 0.5)",
                  },
                },
              },
            ],
          };
          myChart.setOption(option);
        });
      option && myChart.setOption(option);
    },
  },
  mounted() {
    this.myTopicAnalysis();
  },
};
</script>

<style scoped>
.topic_analysis {
  position: absolute;
  width: 100%;
  height: 25%;
  top: 20%;
  background-color: #fff;
}
.topic_analysis_title {
  margin: 10px 20px;
  padding: 5px;
  font-weight: 600;
  letter-spacing: 1px;
}
#topic_analysis_graph {
  width: 450px;
  height: 220px;
  position: relative;
  top: -45px;
  left: -20px;
}
</style>