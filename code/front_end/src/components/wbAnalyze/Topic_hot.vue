<template>
  <div class="topic_hot">
    <div class="topic_hot_top">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-redu"></use>
      </svg>
      <span>话题热度</span>
      <div class="radio">
        <el-radio-group v-model="radio">
          <el-radio :label="1">一天</el-radio>
          <el-radio :label="2">一个月</el-radio>
          <el-radio :label="3">三个月</el-radio>
        </el-radio-group>
      </div>
    </div>
    <div id="lineChart"></div>
  </div>
</template>

<script>
export default {
  name: "topic_hot",
  data() {
    return {
      radio: 1,
      one_day_daytime: "",
      one_day_hourtime: [],
      one_day_count: [],
      one_month_time: [],
      one_month_count: [],
      three_month_time: [],
      three_month_count: [],
      myChart: "",
    };
  },
  watch: {
    radio(newradio) {
      this.changeline(newradio);
    },
  },
  methods: {
    getTopicData(id) {
      this.$axios.get("/hot?tag_task_id="+id).then((res) => {
        this.one_day_count = res.data.data.one_day.data_count;
        let time = res.data.data.one_day.data_time;
        this.one_day_daytime = time[0].split("T")[0];
        for (let index in time) {
          this.one_day_hourtime[index] = time[index].split("T")[1];
        }
        this.one_month_count = res.data.data.one_month.data_count;
        time = res.data.data.one_month.data_time;
        for (let index in time) {
          this.one_month_time[index] = time[index].split("T")[0];
        }
        this.three_month_count = res.data.data.three_month.data_count;
        time = res.data.data.three_month.data_time;
        for (let index in time) {
          this.three_month_time[index] = time[index].split("T")[0];
        }
      });
    },
    myLineChart(time, count) {
      let option;
      if (
        this.myChart != null &&
        this.myChart != "" &&
        this.myChart != undefined
      ) {
        this.myChart.dispose(); //解决echarts dom已经加载的报错
      }
      this.myChart = this.$echarts.init(document.getElementById("lineChart"));
      option = {
        tooltip: {
          trigger: "axis",
          position: "center",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#6a7985",
            },
          },
        },
        xAxis: {
          type: "category",
          data: time,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: count,
            type: "line",
          },
        ],
      };
      this.myChart.setOption(option);
      option && this.myChart.setOption(option);
    },
    changeline(line) {
      if (line == 1) {
        this.myLineChart(this.one_day_hourtime, this.one_day_count);
      } else if (line == 2) {
        this.myLineChart(this.one_month_time, this.one_month_count);
      } else {
        this.myLineChart(this.three_month_time, this.three_month_count);
      }
    },
  },
  mounted() {
    this.$bus.$on("send_tag_task_id", (tag_task_id) => {
      console.log("这里是折线图组件,收到了数据:", tag_task_id);
      this.getTopicData(tag_task_id);
    });
    setTimeout(() => {
      this.myLineChart(this.one_day_hourtime, this.one_day_count);
    }, 2000);
  },
  beforeDestroy() {
    this.$bus.$off("send_tag_task_id");
  },
};
</script>

<style scpoed>
.topic_hot {
  background-color: #fff;
  height: 41%;
  position: relative;
}
#lineChart {
  left: 20px;
  width: 1000px;
  height: 400px;
}
.topic_hot_top {
  height: 10%;
  margin-left: 20px;
}
.topic_hot_top .radio {
  position: absolute;
  right: 10px;
  top: 10px;
}
.el-radio {
  z-index: 99;
}
</style>