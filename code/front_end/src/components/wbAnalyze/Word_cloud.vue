<template>
  <div class="word_cloud">
    <div class="word_cloud_top">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-ciyuntu"></use>
      </svg>
      <span class="title_text"> 词云 </span>
    </div>
    <div class="show_words">
      <div id="chars_word_cloud"></div>
    </div>
  </div>
</template>

<script>
export default {
  name: "word_cloud",
  data() {
    return {
      timer: "",
      myChart: "",
      cloud_word: "",
    };
  },
  methods: {
    getCloudWord(id) {
      this.$axios.get("word_cloud?tag_task_id=" + id).then((res) => {
        console.log(res.data)
        this.cloud_word = res.data.data.data;
        this.myWordCloud(res.data.data.data);
      });
    },
    myWordCloud(data) {
      let option;
      if (
        this.myChart != null &&
        this.myChart != "" &&
        this.myChart != undefined
      ) {
        this.myChart.dispose(); //解决echarts dom已经加载的报错
      }
      this.myChart = this.$echarts.init(
        document.getElementById("chars_word_cloud")
      );
      // 指定图表的配置项和数据
      option = {
        tooltip: {
          show: true,
        },
        series: [
          {
            type: "wordCloud",
            sizeRange: [10, 50], //文字范围
            //文本旋转范围，文本将通过rotationStep45在[-90,90]范围内随机旋转
            rotationRange: [-45, 90],
            rotationStep: 45,
            textRotation: [0, 45, 90, -45],
            //形状
            textStyle: {
              color: function () {
                //文字颜色的随机色
                return (
                  "rgb(" +
                  [
                    Math.round(Math.random() * 200),
                    Math.round(Math.random() * 100),
                    Math.round(Math.random() * 300),
                  ].join(",") +
                  ")"
                );
              },
            },
            data: data,
          },
        ],
      };
      this.myChart.setOption(option);
      // 使用刚指定的配置项和数据显示图表。
      option && this.myChart.setOption(option);
    },
  },
  mounted() {

    this.$bus.$on("send_tag_task_id", (tag_task_id) => {
      console.log("这里是词云组件,收到了数据:", tag_task_id);
      this.getCloudWord(tag_task_id);
    });
    this.timer = setInterval(() => {
      this.myWordCloud(this.cloud_word);
    }, 5000);
  },
  beforeDestroy() {
    this.$bus.$off("send_tag_task_id");
    clearInterval(this.timer);
    this.timer = null;
  },
};
</script>

<style scpoed>
.word_cloud {
  position: absolute;
  width: 100%;
  height: 30%;
  background-color: #fff;
}
.word_cloud_top {
  margin-left: 10px;
}
.w_title {
  padding-top: 10px;
  height: 50px;
  text-align: center;
  font-size: 20px;
}
#chars_word_cloud {
  width: 400px;
  height: 200px;
  top: -10px;
}
.icon {
  position: relative;
  top: 8px;
}
</style>