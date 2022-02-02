<template>
  <div class="wbAnalyze">
    <div class="side">
      <SideBorder />
    </div>
    <div class="container">
      <div class="top">
        <Search />
      </div>
      <div class="main">
        <div class="left">
          <DefaultPanel />
        </div>
        <div class="center">
          <div class="blog_hot">
            <BlogHot />
          </div>
          <div class="topic_hot">
            <TopicHot />
          </div>
        </div>
        <div class="right">
          <div class="word">
            <WordCloud />
          </div>
          <div class="graph">
            <RelationGraph />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import SideBorder from "../components/Side_border";
import BlogHot from "../components/wbAnalyze/Blog_hot";
import DefaultPanel from "../components/wbAnalyze/Default_panel";
import RelationGraph from "../components/wbAnalyze/Relation_graph";
import Search from "../components/wbAnalyze/Search";
import TopicHot from "../components/wbAnalyze/Topic_hot";
import WordCloud from "../components/wbAnalyze/Word_cloud";

export default {
  name: "wbAnalyze",
  components: {
    BlogHot,
    DefaultPanel,
    RelationGraph,
    Search,
    TopicHot,
    WordCloud,
    SideBorder,
  },
};
</script>

<style scoped>
.wbAnalyze {
  width: 100%;
  display: flex;
  height: 100%;
}
.side {
  width: 50px;
}
.container {
  background-color: #eee;
  width: 100%;
  height: 100%;
}
.top {
  height: 6%;
}
.main {
  margin: 10px 10px 0;
  height: 92%;
}
.left {
  height: 100%;
  width: 15%;
  float: left;
}
.center {
  height: 100%;
  float: left;
  width: 55%;
  margin: 0 10px;
  position: relative;
}
.right {
  height: 100%;
  width: 27.5%;
  float: left;
  position: relative;
}
.blog_hot {
  width: 100%;
  margin-bottom: 10px;
}
.topic_hot {
  width: 100%;
}
.word {
  width: 100%;
  margin-bottom: 10px;
}
.graph {
  width: 100%;
}
</style>