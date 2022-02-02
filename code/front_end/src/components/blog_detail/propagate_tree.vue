<template>
  <div class="propagate_tree">
    <div class="propagate_tree_title">传播树</div>
    <el-button type="text" @click="show" class="maxTree"
      >点击打开 Dialog</el-button
    >
    <div id="propagate_tree_graph"></div>
    <el-dialog
      title="传播树大图"
      :visible.sync="dialogVisible"
      fullscreen="true"
    >
      <div id="tree"></div>
      <span slot="footer" class="dialog-footer">
        <el-button type="primary" @click="dialogVisible = false"
          >确 定</el-button
        >
      </span>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "propagate_tree",
  data() {
    return {
      dialogVisible: false,
    };
  },
  methods: {
    myPropagate_tree() {
      let myChart = this.$echarts.init(
        document.getElementById("propagate_tree_graph")
      );
      let option;
      let query = this.$route.query;
      myChart.showLoading();
      this.$axios.get("/comment/tree?tag_task_id="+query.tag_task_id+"&weibo_id="+query.weibo_id).then((res) => {
        myChart.hideLoading();
        console.log(res.data)
        res.data.data.data.children.forEach(function (datum, index) {
          index % 2 === 0 && (datum.collapsed = true);
        });
        myChart.setOption(
          (option = {
            tooltip: {
              trigger: "item",
              triggerOn: "mousemove",
            },
            series: [
              {
                type: "tree",
                data: [res.data.data.data],
                top: "1%",
                left: "10%",
                bottom: "1%",
                right: "20%",
                symbolSize: 7,
                label: {
                  position: "left",
                  verticalAlign: "middle",
                  align: "right",
                  fontSize: 9,
                },
                leaves: {
                  label: {
                    position: "right",
                    verticalAlign: "middle",
                    align: "left",
                  },
                },
                emphasis: {
                  focus: "descendant",
                },
                expandAndCollapse: true,
                animationDuration: 550,
                animationDurationUpdate: 750,
              },
            ],
          })
        );
      });

      option && myChart.setOption(option);
    },
    show() {
      this.dialogVisible = true;
      this.$nextTick(function () {
        let myChart = this.$echarts.init(document.getElementById("tree"));
        let option;
        myChart.showLoading();
        let query = this.$route.query;
        this.$axios.get("/comment/tree?tag_task_id="+query.tag_task_id+"&weibo_id="+query.weibo_id).then((res) => {
          myChart.hideLoading();
          res.data.data.data.children.forEach(function (datum, index) {
            index % 2 === 0 && (datum.collapsed = true);
          });
          myChart.setOption(
            (option = {
              tooltip: {
                trigger: "item",
                triggerOn: "mousemove",
              },
              series: [
                {
                  type: "tree",
                  data: [res.data.data.data],
                  top: "1%",
                  left: "10%",
                  bottom: "1%",
                  right: "20%",
                  symbolSize: 7,
                  label: {
                    position: "left",
                    verticalAlign: "middle",
                    align: "right",
                    fontSize: 9,
                  },
                  leaves: {
                    label: {
                      position: "right",
                      verticalAlign: "middle",
                      align: "left",
                    },
                  },
                  emphasis: {
                    focus: "descendant",
                  },
                  // orient: "vertical",
                  expandAndCollapse: true,
                  animationDuration: 550,
                  animationDurationUpdate: 750,
                },
              ],
            })
          );
        });

        option && myChart.setOption(option);
      });
    },
  },
  mounted() {
    this.myPropagate_tree();
  },
};
</script>

<style scoped>
.propagate_tree {
  position: absolute;
  top: 1%;
  width: 100%;
  height: 99%;
  background-color: #fff;
}
.propagate_tree_title {
  margin-left: 20px;
  padding: 5px;
  font-weight: 600;
  letter-spacing: 1px;
}
#propagate_tree_graph {
  width: 550px;
  height: 750px;
  top: 30px;
  margin-left: 10%;
}
.maxTree {
  position: absolute;
  right: 10px;
  top: 10px;
  z-index: 99;
}
#tree {
  width: 1800px;
  height: 1000px;
}
</style>