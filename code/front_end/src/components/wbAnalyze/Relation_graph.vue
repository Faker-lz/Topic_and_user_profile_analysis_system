<template>
  <div class="relation_graph">
    <div class="relation_graph_top" @click="ToPersonList">
      <svg class="icon" aria-hidden="true">
        <use xlink:href="#icon-wangluoguanxitu"></use>
      </svg>
      <span>关系图</span>
    </div>
    <div id="show_graph"></div>
  </div>
</template>

<script>
export default {
  name: "relation_graph",
  data() {
    return {
      categories: [
        {
          name: "正常用户",
        },
        // {
        //   name: "水军",
        // },
      ],
    };
  },
  methods: {
    myRelationGraph(id) {
      let option;
      let myChart = this.$echarts.init(document.getElementById("show_graph"));
      myChart.showLoading();
      this.$axios.get("relation_graph?tag_task_id="+id).then((res) => {
        console.log(res.data.data)
        let nodes = res.data.data.nodes_list;
        for (let index in nodes) {
          nodes[index].id = index;
        }
        let links = res.data.data.links_list;
        links.forEach((link) => {
          for (let node of nodes) {
            if (link.source == node.name) {
              link.source = node.id;
              node.show = true;
            }
            if (link.target == node.name) {
              link.target = node.id;
              node.show = true;
            }
          }
        });
        let newNodes = [];
        for(let n in nodes){
          if(nodes[n].show){
            newNodes.push(nodes[n])
          }
        }
        console.log(newNodes);
        console.log(links);
        myChart.hideLoading();
        nodes.forEach(function (node) {
          node.label = {
            show: node.value > 10,
          };
        });
        option = {
          title: {
            text: "用户关系图",
            subtext: "Default layout",
            top: "bottom",
            left: "right",
          },
          tooltip: {},
          legend: [
            {
              data: this.categories.map(function (a) {
                return a.name;
              }),
            },
          ],
          animationDuration: 1500,
          animationEasingUpdate: "quinticInOut",
          series: [
            {
              name: "用户关系图",
              type: "graph",
              layout: "force",
              data: newNodes,
              links: links,
              categories: this.categories,
              roam: true,
              label: {
                position: "right",
                formatter: "{b}",
              },
              lineStyle: {
                color: "source",
                curveness: 0.3,
              },
              emphasis: {
                focus: "adjacency",
                lineStyle: {
                  width: 10,
                },
              },
            },
          ],
        };
        myChart.setOption(option);
      });
      option && myChart.setOption(option);
    },
    ToPersonList() {
      this.$router.push({
        path: "/person_list",
        query: {
          tag_task_id: this.tid,
        },
      });
    },
  },
  mounted() {
    let res = Array.from(new Array(5), () => []);
    console.log(res);
    this.$bus.$on("send_tag_task_id", (tag_task_id) => {
      console.log("这里是关系图组件,收到了数据:", tag_task_id);
      this.tid = tag_task_id;
      this.myRelationGraph(tag_task_id);

    });
  },
  beforeDestroy() {
    this.$bus.$off("send_tag_task_id");
  },
};
</script>

<style scpoed>
.relation_graph_top {
  margin-left: 10px;
}
.relation_graph {
  background-color: #fff;
  position: absolute;
  top: 31%;
  width: 100%;
  height: 68%;
}
#show_graph {
  height: 500px;
  width: 400px;
}
</style>