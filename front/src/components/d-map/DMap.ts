import { Component, Prop, Vue, Watch } from 'vue-property-decorator';
import L from "leaflet";
import "leaflet.heat";
import { MVC } from '@/types';

const heatmapConfig: Object = {
  scaleRadius: true,
  radius: 10,
  minOpacity: 0.25,
  max_val: 1,
  gradient: { 0: "white", 0.25: "yellow", 0.5: "orange", 1: "red" }
};

@Component({})
export default class DMap extends Vue {
  name: String = "dtp-map";
  url: string = "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png";
  attribution: string | string[] = '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors';
  canvas: L.Canvas = L.canvas();
  tileLayerOptions: L.TileLayerOptions = {}
  tileLayer: L.TileLayer = L.tileLayer(this.url, this.tileLayerOptions)
  mvcPointsLayer: L.FeatureGroup = new L.FeatureGroup()
  mapOptions: L.MapOptions = {
    zoomSnap: 0.5,
    renderer: this.canvas
    // attribution: this.attribution
  };
  map: L.Map = L.map("map", this.mapOptions);
  zoom: Number = 10;
  maxZoom: Number = 15;
  bounds: null | undefined;
  currentZoom: Number = 11.5;
  currentCenter: Object = { lat: 54.19, lng: 45.18 };
  showParagraph: Boolean = false;

  // @Prop() private handleZoomChange!: Function;
  @Prop() private handleZoomStart: L.LeafletEventHandlerFn = () => { };
  @Prop() private handleZoomEnd: L.LeafletEventHandlerFn = () => { };
  @Prop() private handleMounted: Function = () => { };
  @Prop() private mvcs!: Array<MVC>;
  @Prop() private center: L.LatLngExpression = { lat: 54.19, lng: 45.18 }

  mounted() {

    this.map.setView(this.center, 3);
    this.map.addLayer(this.tileLayer);

    this.map.on("zoomend moveend", this.handleZoomEnd);
    this.map.on("zoomstart", this.handleZoomStart);
    // this.$refs.map.on("resize moveend zoomend", this.handleZoomEnd);

    this.handleMounted(this.zoom, this.map.getBounds());
  }
//   computed: {
//     showHeatMap() {
//       return this.zoom < this.maxZoom ? true : false;
//     }
//   };
//   // watch: {
//   @Watch() points!: {
//     console.log("Points updated");
//     this.drawPoints();
//   };
//     points() {
//     },
//     center(val) {
//       if (
//         val != null &&
//         (val.lat != this.currentCenter.lat || val.lng != this.currentCenter.lng)
//       ) {
//         this.$refs.map.setView(val, 12);
//       }
//       this.currentCenter = val;
//     }
//   // };

//   methods: {
//     drawPoints() {
//       console.log("Draw points");
//       console.log(`Count points: ${this.points.length}`);

//       if (this.$refs.mvcPointsLayer) {
//         console.log("Draw points::Clear layers");
//         this.$refs.mvcPointsLayer.clearLayers();
//       }
//       if (this.showHeatMap) {
//         if (!this.$refs.heatmapLayer) {
//           this.$refs.heatmapLayer = new L.HeatLayer(this.points, heatmapConfig);
//         }
//         this.$refs.map.removeLayer(this.$refs.mvcPointsLayer);
//         this.$refs.map.addLayer(this.$refs.heatmapLayer);
//         this.$refs.heatmapLayer.setLatLngs(this.points);
//       } else {
//         this.points.forEach(point => {
//           let marker = new L.circleMarker([point.lat, point.lng], {
//             radius: 4,
//             color: point.color
//           });
//           // marker.bindTooltip(`${point.region}<br>${point.datetime}<br>${point.lat} - ${point.lng}`);
//           this.$refs.mvcPointsLayer.addLayer(marker);
//         });
//         if (this.$refs.heatmapLayer !== undefined) {
//           this.$refs.map.removeLayer(this.$refs.heatmapLayer);
//         }
//         this.$refs.map.addLayer(this.$refs.mvcPointsLayer);
//       }
//     },
//     handleZoomEnd() {
//       console.log("Handle zoom end");

//       this.bounds = this.$refs.map.getBounds();
//       this.zoom = this.$refs.map.getZoom();
//       this.currentCenter = this.$refs.map.getCenter();

//       let _params = {
//         ne_lat: this.bounds._northEast.lat,
//         ne_lng: this.bounds._northEast.lng,
//         sw_lat: this.bounds._southWest.lat,
//         sw_lng: this.bounds._southWest.lng
//       };

//       let params = { ...this.$route.query, ..._params };
//       this.$router.push({ name: "Area", query: params });
//       this.drawPoints();
//       this.handleZoomChange();
//     }
//   }
// };
// </script>

// <script>
// import Vue from "vue";
// import L from "leaflet";
// import "leaflet.heat";


// export default Vue.extend({
//   name: "dtp-map",

//   props: {
//     handleZoomChange: Function,
//     handleZoomStart: Function,
//     handleMounted: Function,
//     points: Array,
//     center: {
//       type: Object,
//       default: L.latLng(54.19, 45.18)
//     }
//   },
//   data() {
//     return {
//       zoom: 10,
//       maxZoom: 15,
//       maxValue: 1,
//       url: mapUrl,

//       attribution:
//         '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
//       bounds: null,
//       currentZoom: 11.5,
//       currentCenter: L.latLng(54.19, 45.18),
//       showParagraph: false,
//       mapOptions: {
//         zoomSnap: 0.5
//       }
//     };
//   },
//   mounted() {
//     this.$refs.canvas = L.canvas();
//     this.$refs.map = new L.map("map", {
//       renderer: this.$refs.canvas,
//       attribution: this.attribution
//     });
//     this.$refs.map.setView(this.center, 3);

//     this.$refs.tileLayer = L.tileLayer(mapUrl, { id: "map" });
//     this.$refs.map.addLayer(this.$refs.tileLayer);

//     this.$refs.map.on("zoomend moveend", this.handleZoomEnd);
//     this.$refs.map.on("zoomstart", this.handleZoomStart);
//     // this.$refs.map.on("resize moveend zoomend", this.handleZoomEnd);

//     this.$refs.mvcPointsLayer = new L.FeatureGroup();

//     this.handleMounted(this.zoom, this.$refs.map.getBounds());
//   },
//   computed: {
//     showHeatMap() {
//       return this.zoom < this.maxZoom ? true : false;
//     }
//   },
//   watch: {
//     points() {
//       console.log("Points updated");
//       this.drawPoints();
//     },
//     center(val) {
//       if (
//         val != null &&
//         (val.lat != this.currentCenter.lat || val.lng != this.currentCenter.lng)
//       ) {
//         this.$refs.map.setView(val, 12);
//       }
//       this.currentCenter = val;
//     }
//   },

//   methods: {
//     drawPoints() {
//       console.log("Draw points");
//       console.log(`Count points: ${this.points.length}`);

//       if (this.$refs.mvcPointsLayer) {
//         console.log("Draw points::Clear layers");
//         this.$refs.mvcPointsLayer.clearLayers();
//       }
//       if (this.showHeatMap) {
//         if (!this.$refs.heatmapLayer) {
//           this.$refs.heatmapLayer = new L.HeatLayer(this.points, heatmapConfig);
//         }
//         this.$refs.map.removeLayer(this.$refs.mvcPointsLayer);
//         this.$refs.map.addLayer(this.$refs.heatmapLayer);
//         this.$refs.heatmapLayer.setLatLngs(this.points);
//       } else {
//         this.points.forEach(point => {
//           let marker = new L.circleMarker([point.lat, point.lng], {
//             radius: 4,
//             color: point.color
//           });
//           // marker.bindTooltip(`${point.region}<br>${point.datetime}<br>${point.lat} - ${point.lng}`);
//           this.$refs.mvcPointsLayer.addLayer(marker);
//         });
//         if (this.$refs.heatmapLayer !== undefined) {
//           this.$refs.map.removeLayer(this.$refs.heatmapLayer);
//         }
//         this.$refs.map.addLayer(this.$refs.mvcPointsLayer);
//       }
//     },
//     handleZoomEnd() {
//       console.log("Handle zoom end");

//       this.bounds = this.$refs.map.getBounds();
//       this.zoom = this.$refs.map.getZoom();
//       this.currentCenter = this.$refs.map.getCenter();

//       let _params = {
//         ne_lat: this.bounds._northEast.lat,
//         ne_lng: this.bounds._northEast.lng,
//         sw_lat: this.bounds._southWest.lat,
//         sw_lng: this.bounds._southWest.lng
//       };

//       let params = { ...this.$route.query, ..._params };
//       this.$router.push({ name: "Area", query: params });
//       this.drawPoints();
//       this.handleZoomChange();
//     }
//   }
// });
}
