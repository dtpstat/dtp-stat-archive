<template>
  <div class="map-section collapse show flex-grow-1" data-parent=".map-with-stats">
    {{showHeatMap}}
    {{currentZoom}}
    <div id="map" style="height: 765px; position: relative;"></div>
  </div>
</template>

<script>
import L from "leaflet";
import "leaflet.heat";

const mapUrl =
  "https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png";

const heatmapConfig = {
  scaleRadius: true,
  radius: 20,
  minOpacity: 0.1,
  max_val: 1,
  gradient: { 0: "white", 0.25: "yellow", 0.5: "orange", 1: "red" }
};

export default {
  name: "dtp-map",

  props: {
    handleZoomChange: Function,
    handleMounted: Function,
    points: Array,
    center: Array
  },
  data() {
    return {
      points: [],
      zoom: 10,
      maxZoom: 15,
      maxValue: 1,
      url: mapUrl,

      attribution:
        '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      bounds: null,
      currentZoom: 11.5,
      currentCenter: L.latLng(54.19, 45.18),
      showParagraph: false,
      mapOptions: {
        zoomSnap: 0.5
      }
    };
  },
  mounted() {
    this.$refs.canvas = L.canvas();
    this.$refs.map = new L.map("map", {
      renderer: this.$refs.canvas,
      attribution: this.attribution
    });
    this.$refs.map.setView(this.currentCenter, 12);

    this.$refs.tileLayer = L.tileLayer(mapUrl, { id: "map" });
    this.$refs.map.addLayer(this.$refs.tileLayer);

    this.$refs.map.on("zoomend", this.handleZoomEnd);
    // this.$refs.map.on("resize moveend zoomend", this.handleZoomEnd);

    this.$refs.mvcPointsLayer = new L.FeatureGroup();

    var promise = new Promise((resolve, reject) => {
      this.handleMounted(this.zoom, this.$refs.map.getBounds());
    });
    promise.then();
  },
  computed: {
    showHeatMap() {
      return this.currentZoom < this.maxZoom ? true : false;
    }
  },
  watch: {
    points(val) {
      console.log("Points updated");
      this.drawPoints();
    }
  },
  methods: {
    drawPoints() {
      console.log("Draw points");

      if (this.$refs.mvcPointsLayer) {
        this.$refs.mvcPointsLayer.clearLayers();
      }
      if (this.showHeatMap) {
        if (this.$refs.heatmapLayer == undefined) {
          this.$refs.heatmapLayer = new L.HeatLayer(this.points, heatmapConfig);
        }
        this.$refs.map.removeLayer(this.$refs.mvcPointsLayer);
        this.$refs.map.addLayer(this.$refs.heatmapLayer);
      } else {
        this.points.forEach(point => {
          let marker = new L.circleMarker([point.lat, point.lng], {
            radius: 4,
            color: point.color
          });
          // marker.bindTooltip(`${point.region}<br>${point.datetime}<br>${point.lat} - ${point.lng}`);
          this.$refs.mvcPointsLayer.addLayer(marker);
        });
        if (this.$refs.heatmapLayer !== undefined) {
          this.$refs.map.removeLayer(this.$refs.heatmapLayer);
        }
        this.$refs.map.addLayer(this.$refs.mvcPointsLayer);
      }
    },
    handleZoomEnd() {
      console.log("Handle zoom end");

      let bounds = this.$refs.map.getBounds();
      this.currentZoom = this.$refs.map.getZoom();

      let _params = {
        ne_lat: bounds._northEast.lat,
        ne_lng: bounds._northEast.lng,
        sw_lat: bounds._southWest.lat,
        sw_lng: bounds._southWest.lng
      };

      let params = { ...this.$route.query, ..._params };
      this.$router.push({ name: "Area", query: params });
      this.drawPoints();
      this.handleZoomChange();
    },
    centerUpdate(center) {
      this.currentCenter = center;
    },
    showLongText() {
      this.showParagraph = !this.showParagraph;
    },
    innerClick() {
      alert("Click!");
    }
  }
};
</script>