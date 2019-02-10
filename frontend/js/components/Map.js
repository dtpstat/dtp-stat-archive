import React, { Component } from 'react';
import PropTypes from 'prop-types';
import L from 'leaflet';
import HeatmapOverlay from 'leaflet-heatmap';
import {getColorByParticipantTypeId, getMvcTypeName, mvcHasDeadParticipants} from '../services/mvcs';

const MAP_ID = 'dtp-map';
const markerMinRadius = 5;
const markerMaxRadius = 15;

const heatmapConfig = {
    scaleRadius: true,
    radius: 0.001,
    minOpacity: 0.1,
    max_val: 1,
    gradient: {0: 'white',0.25: 'yellow', 0.5: 'orange', 1: 'red'}
};

export default class Map extends Component {
    constructor(props) {
        super(props);
        this.map = null;
        this.mvcPointsLayer = null;
        this.mapObjectsMarkersLayer = null;
        this.mapObjectsMarkers = [];
        this.markers = [];
        this.isPointsLayerShown = false;

        this.setRef = this.setRef.bind(this);
        this.handleLayerClick = this.handleLayerClick.bind(this);
        this.handleZoomEnd = this.handleZoomEnd.bind(this);
        this.handleMapChanges = this.handleMapChanges.bind(this);


        this.state = {
            markers: []
        };
    }

    componentDidMount() {
        this.adjustMapHeight();
        this.initLeaflet();
        this.drawLayers(this.props.mvcs);
    }

    shouldComponentUpdate() {
        return false;
    }

    componentWillReceiveProps(nextProps) {
        if (nextProps.mvcs === this.props.mvcs && nextProps.mapObjectsMarkersData === this.props.mapObjectsMarkersData) {
            return;
        }
        this.drawLayers(nextProps.mvcs, nextProps.mapObjectsMarkersData);
    }

    adjustMapHeight() {
        let $element = $(this.element);
        let $parent = $(this.element.parentElement);

        $element.height($parent.height());
    }

    drawLayers(mvcs, mapObjectsMarkersData) {
        if (this.mvcPointsLayer) {
            this.mvcPointsLayer.clearLayers();
        }
        if (this.heatmapLayer) {
            this.map.removeLayer(this.heatmapLayer);
        }
        if (mvcs.length === 0) {
            return;
        }

        // if map objects was shown before, delete them first
        if (this.mapObjectsMarkers) {
            this.mapObjectsMarkers.forEach(marker => {
                this.map.removeLayer(marker);
            });
        }

        this.createMvcPointsLayer(mvcs);
        this.createHeatmapLayer(mvcs);

        this.setLayerBasedOnZoom(mvcs);

        this.createMapObjectsMarkers(mapObjectsMarkersData || [])
    }
    createMapObjectsMarkers(mapObjectsMarkersData){
        // This method will create markers and show loaded objects on map
        mapObjectsMarkersData.forEach(marker => {
            let mapObjectMarker = L.marker([marker.latitude, marker.longitude])
                    .addTo(this.map)
                    .bindPopup(marker.name)
                    .openPopup();

            this.mapObjectsMarkers.push(mapObjectMarker)
        });
    }

    createMvcPointsLayer(mvcs) {
        this.mvcPointsLayer = new L.FeatureGroup();
        this.markers = [];
        this.canvasRenderer = L.canvas({ padding: 0.5 });
        mvcs.forEach(mvc => {
            let marker = new L.circleMarker([mvc.latitude, mvc.longitude], this.getMarkerOptions(mvc));
            const date = moment(mvc.datetime);
            const actionName = getMvcTypeName(mvc, this.props.dictionaries);
            const tooltipText = `${date.format('DD.MM.YYYY HH:mm')}<br/>${actionName}<br/>Пострадали - ${mvc.injured}, погибли - ${mvc.dead}`;

            marker.bindTooltip(tooltipText);
            this.mvcPointsLayer.addLayer(marker);
            this.markers.push(marker);
        });

        this.mvcPointsLayer.on('click', this.handleLayerClick);
    }

    createHeatmapLayer(mvcs) {
        console.log(mvcs.length);
        const heatmapLayer = new HeatmapOverlay(heatmapConfig);

        const pointValue = 1;

        const data = mvcs.map(mvc => ({
            lat: mvc.latitude,
            lng: mvc.longitude,
            value: pointValue,
        }));

        heatmapLayer.setData({
            max: 2,
            data
        });

        this.heatmapLayer = heatmapLayer;
    }

    setLayerBasedOnZoom(mvcs) {
        const zoom = this.map.getZoom();
        if (zoom < 15 && mvcs.length > 1000) {
            console.log(this.heatmapLayer);
            this.map.removeLayer(this.mvcPointsLayer);
            this.map.addLayer(this.heatmapLayer);
            this.isPointsLayerShown = false;
        } else {
            this.map.removeLayer(this.heatmapLayer);
            this.map.addLayer(this.mvcPointsLayer);
            this.isPointsLayerShown = true;
        }
    }

    getMarkerOptions(mvc) {
        const color = getColorByParticipantTypeId(
            mvc.participant_type_id, 
            this.props.dictionaries.mvc_participant_types
        );
        let radius = this.calcMarkerRadius(mvc);
        let options = {
            color,
            weight: 0,
            opacity: 0.5,
            fill: true,
            fillColor: color,
            fillOpacity: 1,
            radius,
            mvc,
            renderer: this.canvasRenderer
        };

        if (mvcHasDeadParticipants(mvc)) {
            options.color = '#000000';
            options.weight = 2;
        }

        return options;
    }


    calcMarkerRadius(mvc) {
        let radius = markerMinRadius + mvc.participants.length * 0.5;
        if (radius > markerMaxRadius) {
            radius = markerMaxRadius;
        }
        return radius;
    }

    handleZoomEnd() {
        this.setLayerBasedOnZoom(this.props.mvcs);
    }

    handleMapChanges(event){
        if (this.props.onMapChanges) {
            const zoom = this.map.getZoom()
            const center = this.map.getCenter()
            this.props.onMapChanges({
                zoom: zoom,
                center: center
            });
        }
    }

    initLeaflet() {
        const map = L.map(MAP_ID);
        const osmUrl = 'https://cartodb-basemaps-{s}.global.ssl.fastly.net/light_all/{z}/{x}/{y}{r}.png';
        const osm = new L.TileLayer(
            osmUrl, {
                attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
            }
        );
        const {lat, lng, zoom} = this.props.searchParams;
        if (lat && lng && zoom){
            map.setView(new L.LatLng(lat, lng), zoom);
        }
        else {
            let {latitude, longitude} = this.props.defaultCoord;
            const zoom = this.getZoomByRegionLevel(this.props.regionLevel);
            map.setView(new L.LatLng(latitude, longitude), zoom);
        }
        map.addLayer(osm);
        map.on('resize moveend zoomend', this.handleMapChanges);
        map.on('zoomend', this.handleZoomEnd);

        this.map = map;

        if (this.props.onMapReady) {
            this.props.onMapReady(map);
        }
    }


    getZoomByRegionLevel(regionLevel) {
        if (regionLevel >= 2) {
            return 14;
        }
        return 10;
    }

    handleLayerClick(event) {
        if (event.layer && event.layer.options.mvc && this.props.onMvcSelected) {
            this.props.onMvcSelected(event.layer.options.mvc);
        }
    }

    setRef(ref) {
        this.element = ref;
    }

    render() {
        return <div id={MAP_ID} ref={this.setRef} />;
    }
}

Map.propTypes = {
    defaultCoord: PropTypes.object,
    searchParams: PropTypes.object,
    dictionaries: PropTypes.object,
    mvcs: PropTypes.array,
    onMapReady: PropTypes.func,
    onMvcSelected: PropTypes.func,
    onMapChanges: PropTypes.func,
    regionLevel: PropTypes.number,
};
