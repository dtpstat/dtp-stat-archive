import { Component, Prop, Vue } from 'vue-property-decorator';
import axios from "axios";
import L from "leaflet";
import { BriefType, MVC } from "@/types"

import DTPMap from "@/components/dtp-map/DTPMap.vue";
import DTPBrief from "@/components/dtp-brief/DTPBrief";
// import DTPExtraStats from "@/components/DTPExtraStats";
// import DTPPanelOverlay from "@/components/DTPPanelOverlay";
// import DTPMvcDetail from "@/components/DTPMvcDetail";

@Component({
    components: {
        "dtp-map": DTPMap,
        "dpt-brief": DTPBrief,
        // "dtp-extra-stats": DTPExtraStats,
        // "dtp-panel-overlay": DTPPanelOverlay
    }
})
export default class DTPArea extends Vue {
    cancel!: Function
    requestStarted: Boolean = false
    mvcs!: MVC[]|undefined
    region: string | string[] = ''
    parent_region: string | string[] = ''
    region_name: string | string[] = ''
    parent_region_name: string | string[] = ''

    center: Object = { lat: 54.19, lng: 45.18 }
    brief: BriefType = {
        dead: 0,
        deadAuto: 0,
        deadBicycle: 0,
        deadPedestrian: 0,
        injured: 0,
        injuredAuto: 0,
        injuredBicycle: 0,
        injuredPedestrian: 0,
        mvcCount: 0
    }
    mounted() {
        axios.defaults.headers.post["Access-Control-Allow-Origin"] = "*";
    }
    updatePoints(mvcs: MVC[]) {
        console.log("Update points");
        this.mvcs = mvcs;
    }
    cancelRequest() {
        if (this.requestStarted) {
            this.requestStarted = false;
            this.cancel("Operation canceled by the user.");
        }
    }
    updateData() {
        console.log("Update data");
        if (
            (!("region" in this.$route.query) &&
                !("region_name" in this.$route.query) &&
                !("parent_region" in this.$route.query) &&
                !("parent_region_name" in this.$route.query)) ||
            (("region" in this.$route.query) &&
                (this.$route.query.region !== this.region)) ||
            (("region_name" in this.$route.query) &&
                (this.$route.query.region_name !== this.region_name)) ||
            (("parent_region" in this.$route.query) &&
                (this.$route.query.parent_region !== this.parent_region)) ||
            (("parent_region_name" in this.$route.query) &&
                (this.$route.query.parent_region_name !== this.parent_region_name))
        ) {
            this.requestStarted = true;
            let self = this;
            axios
                .get("http://localhost:8000/api/v1/mvc/", {
                    params: this.$route.query,
                    cancelToken: new axios.CancelToken(function executor(c) {
                        self.cancel = c;
                    })
                })
                .then(response => {
                    this.requestStarted = false;
                    this.region = this.$route.query.region;
                    this.parent_region = this.$route.query.parent_region;
                    this.region_name = this.$route.query.region_name;
                    this.parent_region_name = this.$route.query.parent_region_name;
                    this.updatePoints(response.data.result);
                    this.center = response.data.center;
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
