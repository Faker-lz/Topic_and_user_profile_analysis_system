<template>
  <div class="blog_detail">
    <div class="side">
      <SideBorder />
    </div>
    <div class="detail_contain">
      <div class="blog_detail_left">
        <div class="left_blog_info">
          <BlogInfo />
        </div>
        <div class="left_development_trend">
          <DevelopmentTrend />
        </div>
        <div class="left_essential_node">
          <EssentialNode />
        </div>
      </div>
      <div class="blog_detail_center">
        <PropagateTree />
      </div>
      <div class="blog_detail_right">
        <div class="right_cloud_graph">
          <CloudGraph />
        </div>
        <div class="right_topic_analysis">
          <TopicAnalysis />
        </div>
        <div class="right_hot_point">
          <HotPoint />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideBorder from "../components/Side_border";
import BlogInfo from "../components/blog_detail/blog_info";
import CloudGraph from "../components/blog_detail/cloud_graph";
import DevelopmentTrend from "../components/blog_detail/development_trend";
import EssentialNode from "../components/blog_detail/essential_node";
import HotPoint from "../components/blog_detail/hot_point";
import PropagateTree from "../components/blog_detail/propagate_tree";
import TopicAnalysis from "../components/blog_detail/topic_analysis";
export default {
  name: "blog_detail",
  components: {
    SideBorder,
    BlogInfo,
    CloudGraph,
    DevelopmentTrend,
    EssentialNode,
    HotPoint,
    PropagateTree,
    TopicAnalysis,
  },
};
</script>

<style>
.blog_detail {
  width: 100%;
  display: flex;
  height: 100%;
}
.blog_detail_left,
.blog_detail_right {
  float: left;
  height: 100%;
  width: 30%;
  position: relative;
}
.side {
  width: 50px;
}
.detail_contain {
  background-color: #eee;
  width: 100%;
  height: 100%;
}
.blog_detail_center {
  position: relative;
  width: 37%;
  height: 100%;
  float: left;
  margin: 0 10px;
}
</style>