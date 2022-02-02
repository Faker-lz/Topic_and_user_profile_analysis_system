<template>
  <div class="person_list">
    <div class="side">
      <SideBorder />
    </div>
    <div class="participation_list">
      <ParticipationList />
    </div>
    <div class="participation_graph">
      <ParticipationGraph />
    </div>
  </div>
</template>

<script>
import ParticipationList from "../components/person_list/participation_list";
import ParticipationGraph from "../components/person_list/participation_graph";
import SideBorder from "../components/Side_border";
export default {
  name: "person_list",
  components: {
    ParticipationList,
    ParticipationGraph,
    SideBorder,
  },
};
</script>

<style scoped>
.person_list {
  display: flex;
  width: 100%;
  height: 100%;
  background-color: #eee;
}
.side{
    width: 50px;
}
.participation_list,
.participation_graph {
  float: left;
  position: relative;
  width: 25%;
  height: 100%;
  background-color: #fff;
  margin-left: 0.5%;
}
.participation_graph {
  width: 71%;
}
</style>