<template>
  <div class="flex-grow-1 d-flex flex-column">
    <div class="app container-fluid d-flex flex-grow-1">
      <div class="row no-gutters flex-grow-1">
        <div class="col-sm left-column">
          <div class="map-with-stats d-flex flex-column">
            <dtp-map
              :center="defaultCenter"
              :points="points"
              :handleMounted="updateData"
              :handleZoomChange="updateData"
            ></dtp-map>
            <dtp-brief-stats
              :dead="brief.dead"
              :deadAuto="brief.deadAuto"
              :deadBicycle="brief.deadBicycle"
              :deadPedestrian="brief.deadPedestrian"
              :injured="brief.injured"
              :injuredAuto="brief.injuredAuto"
              :injuredBicycle="brief.injuredBicycle"
              :injuredPedestrian="brief.injuredPedestrian"
              :mvcCount="brief.mvcCount"
              ref="brief"
            ></dtp-brief-stats>
            <dtp-extra-stats></dtp-extra-stats>
          </div>
        </div>
        <div class="col-xl-2 col-lg-3 col-md-4 col-sm-5 right-column">
          <dtp-panel-overlay></dtp-panel-overlay>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import DTPMap from "@/components/DTPMap";
import DTPBriefStats from "@/components/DTPBriefStats";
import DTPExtraStats from "@/components/DTPExtraStats";
import DTPPanelOverlay from "@/components/DTPPanelOverlay";
export default {
  name: "dtp-area",
  data() {
    return {
      defaultCenter: [54.196994, 45.411987],
      points: [],
      region: null,
      parent_region: null,
      brief: {
        dead: 1,
        deadAuto: 1,
        deadBicycle: 1,
        deadPedestrian: 1,
        injured: 1,
        injuredAuto: 1,
        injuredBicycle: 1,
        injuredPedestrian: 1,
        mvcCount: 1
      }
    };
  },
  mounted() {
    axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
  },
  components: {
    "dtp-map": DTPMap,
    "dtp-brief-stats": DTPBriefStats,
    "dtp-extra-stats": DTPExtraStats,
    "dtp-panel-overlay": DTPPanelOverlay
  },
  methods: {
    updatePoints(points) {
      console.log("Update points");
      this.points = points;
    },
    updateData() {
      console.log("Update data");
      // console.log(this.$route.query);
      if (
        ((!("region" in this.$route.query) &
          !("region_name" in this.$route.query) &
          !("parent_region" in this.$route.query) &
          !("parent_region_name" in this.$route.query))|
          (("region" in this.$route.query) &
            (this.$route.query.region != this.region))) |
        (("region_name" in this.$route.query) &
          (this.$route.query.region_name != this.region_name)) |
        (("parent_region" in this.$route.query) &
          (this.$route.query.parent_region != this.parent_region)) |
        (("parent_region_name" in this.$route.query) &
          (this.$route.query.parent_region_name != this.parent_region_name))
      ) {
        axios
          .get("http://localhost:8000/api/v1/mvc/", {
            params: this.$route.query
          })
          .then(response => {
            this.region = this.$route.query.region;
            this.parent_region = this.$route.query.parent_region;
            this.region_name = this.$route.query.region_name;
            this.parent_region_name = this.$route.query.parent_region_name;
            this.updatePoints(response.data.result);
            this.brief.mvcCount = response.data.count;
            this.brief.injured = response.data.injured;
            this.brief.injuredAuto = response.data.injuredAuto;
            this.brief.injuredBicycle = response.data.injuredBicycle;
            this.brief.injuredPedestrian = response.data.injuredPedestrian;
            this.brief.dead = response.data.dead;
            this.brief.deadAuto = response.data.deadAuto;
            this.brief.deadBicycle = response.data.deadBicycle;
            this.brief.deadPedestrian = response.data.deadPedestrian;
          });
      }
    }
  }
};
</script>
