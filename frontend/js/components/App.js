import React, {PureComponent} from 'react';
import PropTypes from 'prop-types';
import Filters from './Filters';
import MvcDetails from './MvcDetails';
import PanelWithOverlay from './PanelWithOverlay';
import MapWithStats from './MapWithStats';
import PreloaderScreen from './PreloaderScreen';
import * as apiAccess from '../services/apiAccess';
import {filterMvcs, getMinMaxDates, getStreetsFromMvcs} from '../services/mvcs';
import {dictionariesToHashMaps, sortDictionaries} from '../services/dictionaries';
import {calcCountsByMvcTypes, calcCountsByOffences, calcInjuredAndDeadCounts} from '../services/stats';
import {calcRangesForDatePicker, getYearRange} from '../services/dates';
import Router from "../services/router";
import createHistory from 'history/createBrowserHistory'

export default class App extends PureComponent {
    constructor(props) {
        super(props);

        this.handleDateRangeChange = this.handleDateRangeChange.bind(this);
        this.handleMvcTypeChange = this.handleMvcTypeChange.bind(this);
        this.handleNearbyChange = this.handleNearbyChange.bind(this);
        this.handleOffenceChange = this.handleOffenceChange.bind(this);
        this.handleStreetChange = this.handleStreetChange.bind(this);
        this.handleParticipantTypeChange = this.handleParticipantTypeChange.bind(this);
        this.handleOnlyDeadChange = this.handleOnlyDeadChange.bind(this);
        this.handleMvcSelected = this.handleMvcSelected.bind(this);
        this.handleMapChanges = this.handleMapChanges.bind(this);
        this.handleMarkers = this.handleMarkers.bind(this);
        this.handleCloseMvc = this.handleCloseMvc.bind(this);
        this.handleShowMap = this.handleShowMap.bind(this);
        this.handleShowStats = this.handleShowStats.bind(this);
        this.handleToggleStats = this.handleToggleStats.bind(this);
        this.handleConditionTypeChange = this.handleConditionTypeChange.bind(this);

        const [fromDate, toDate] = getYearRange();
        this.router = new Router(createHistory({}))
        const params = this.router.get_params()

        this.state = {
            mvcs: null,

            // this variable will consist data of loaded objects from file input,
            // that must be show on map like markers
            mapObjectsMarkersData: null,
            //==============

            dictionaries: null,
            filteredMvcs: null,
            dictionariesAsHashMaps: null,
            streetsFromMvcs: null,
            minDate: null,
            maxDate: null,
            dateRanges: null,
            isDataLoaded: false,
            loadProgress: 0,
            selectedMvc: null,
            showMvcDetails: false,
            filters: {
                fromDate: this.getDate(params.fromDate) || fromDate,
                toDate: this.getDate(params.toDate) || toDate,
                mvcType: +params.mvcType || null,
                nearby: +params.nearby || null,
                offence: +params.offence || null,
                street: +params.street || null,
                participantType: (params.participantType && params.participantType.split('_').map(Number)) || null,
                conditionType: +params.conditionType || null,
                onlyDead: params.onlyDead || false,
            },
            stats: {},
            showStats: false,
            searchParams: params,
        };
    }

    getDate(s) {
        return s && moment(s, "YYYY.MM.DD")
    }

    getUrlParams(params) {
        return Object.assign({}, params, {
            fromDate: moment(params.fromDate).format("YYYY.MM.DD"),
            toDate: moment(params.toDate).format("YYYY.MM.DD"),
            onlyDead: params.onlyDead || undefined,
            participantType: (params.participantType && params.participantType.join('_')) || undefined,
        });
    }
    componentDidMount() {
        let getDictionariesPromise = apiAccess.getDictionaries().then((dictionaries) => {
            dictionaries.conditions = [
                {id: 1, name: "Ночь"} ,
                {id: 2, name: "День"} ,
            ]
            let dictionariesAsHashMaps = dictionariesToHashMaps(dictionaries);
            dictionaries = sortDictionaries(dictionaries);
            this.setState({dictionaries, dictionariesAsHashMaps});
        });

        const {regionAlias, areaAlias} = this.props;
        let getMvcsPromise = apiAccess.getMvcs(regionAlias, areaAlias).then((mvcs) => {
            this.setState({mvcs});
        });

        let getParticipantTypePromise = apiAccess.getParticipantTypes().then((items) => {
            if (this.state.filters.participantType){
                return;
            }
            let participantTypeItem = items.mvc_participant_types.filter(function (item) {
                return item.value === true
            });

            let participantType = participantTypeItem.map(item => item.id);

            let filters = Object.assign({}, this.state.filters, {participantType: participantType});
            this.setState({filters: filters});

        });

        Promise.all([getDictionariesPromise, getMvcsPromise, getParticipantTypePromise]).then(() => this.processLoadedMvcs());
    }

    processLoadedMvcs() {
        let streetsFromMvcs = getStreetsFromMvcs(this.state.mvcs, this.state.dictionariesAsHashMaps.streets);
        let {minDate, maxDate} = getMinMaxDates(this.state.mvcs);
        let dateRanges = calcRangesForDatePicker(minDate, maxDate);
        let filteredMvcs = filterMvcs(this.state.mvcs, this.state.filters);
        let stats = this.calcStats(filteredMvcs);
        this.setState({
            streetsFromMvcs,
            minDate,
            maxDate,
            dateRanges,
            stats,
            filteredMvcs,
        });

        setTimeout(() => this.setState({isDataLoaded: true}), 5);
    }

    calcStats(mvcs) {
        let counts = calcInjuredAndDeadCounts(mvcs);

        counts.mvcCount = mvcs.length;

        counts.countsByMvcTypes = calcCountsByMvcTypes(mvcs, this.state.dictionaries);

        counts.countsByOffences = calcCountsByOffences(mvcs, this.state.dictionaries);

        return counts;
    }

    handleDateRangeChange(start, end) {
        let filters = Object.assign({}, this.state.filters, {fromDate: start, toDate: end});
        this.handleFiltersChange(filters);
    }

    handleOnlyDeadChange(selectedOnlyDead) {
        let filters = Object.assign({}, this.state.filters, {onlyDead: selectedOnlyDead.value});
        this.handleFiltersChange(filters);
    }

    handleParticipantTypeChange(selectedParticipantType) {
        let filters = Object.assign({}, this.state.filters, {participantType: Array.from(selectedParticipantType)});
        this.handleFiltersChange(filters);
    }

    handleMvcTypeChange(selectedMvcType) {
        let selectedMvcTypeId = selectedMvcType ? selectedMvcType.id : null;
        let filters = Object.assign({}, this.state.filters, {mvcType: selectedMvcTypeId});
        this.handleFiltersChange(filters);
    }

    handleConditionTypeChange(selectedConditionType) {
        let selectedConditionTypeId = selectedConditionType ? selectedConditionType.id : null;
        let filters = Object.assign({}, this.state.filters, { conditionType: selectedConditionTypeId });
        this.handleFiltersChange(filters);
    }

    handleNearbyChange(selectedNearby) {
        let selectedNearbyId = selectedNearby ? selectedNearby.id : null;
        let filters = Object.assign({}, this.state.filters, {nearby: selectedNearbyId});
        this.handleFiltersChange(filters);
    }

    handleOffenceChange(selectedOffence) {
        let selectedOffenceId = selectedOffence ? selectedOffence.id : null;
        let filters = Object.assign({}, this.state.filters, {offence: selectedOffenceId});
        this.handleFiltersChange(filters);
    }

    handleStreetChange(selectedStreet) {
        let selectedStreetId = selectedStreet ? selectedStreet.id : null;
        let filters = Object.assign({}, this.state.filters, {street: selectedStreetId});
        this.handleFiltersChange(filters);
    }

    handleMarkers(mapObjectsMarkersData) {
        // this handler got loaded objects data from file input
        // and change state, this will re render map with loaded objects
        this.setState({mapObjectsMarkersData: mapObjectsMarkersData});
    }

    handleFiltersChange(filters) {
        const filteredMvcs = filterMvcs(this.state.mvcs, filters);
        const stats = this.calcStats(filteredMvcs);
        this.setState({filters, filteredMvcs, stats});

        this.router.set_params(this.getUrlParams(filters), false)
    }

    handleMvcSelected(mvc) {
        this.setState({selectedMvc: mvc, showMvcDetails: true});
    }


    handleMapChanges(mapParam) {
        let filters = Object.assign({}, this.state.filters, mapParam);
        this.setState({filters: filters});

        this.router.set_params(this.getUrlParams(filters), true)
    }

    handleCloseMvc() {
        this.setState({showMvcDetails: false});
    }

    handleShowMap() {
        this.setState({showStats: false});
    }

    handleShowStats() {
        this.setState({showStats: true});
    }

    handleToggleStats() {
        this.setState(prevState => ({
            showStats: !prevState.showStats,
        }));
    }

    render() {
        if (!this.state.isDataLoaded) {
            return (
                <PreloaderScreen/>
            );
        }

        const dictionaries = this.state.dictionaries;
        const filters = this.state.filters;

        return (
            <div className="app container-fluid d-flex flex-grow-1">
                <div className="row no-gutters flex-grow-1">
                    <div className="col-sm left-column">
                        <MapWithStats
                            cityName={this.props.cityName}
                            defaultCoord={{latitude: this.props.regionLat, longitude: this.props.regionLon}}
                            searchParams={this.state.searchParams}
                            dictionaries={this.state.dictionariesAsHashMaps}
                            mvcs={this.state.filteredMvcs || this.state.mvcs}
                            mapObjectsMarkersData={this.state.mapObjectsMarkersData}
                            onMvcSelected={this.handleMvcSelected}
                            onMapChanges={this.handleMapChanges}
                            onToggleStats={this.handleToggleStats}
                            regionLevel={this.props.regionLevel}
                            showStats={this.state.showStats}
                            stats={this.state.stats}
                        />
                    </div>
                    <div className="col-xl-2 col-lg-3 col-md-4 col-sm-5 right-column">
                        <PanelWithOverlay
                            overlay={(
                                <MvcDetails
                                    dictionaries={this.state.dictionariesAsHashMaps}
                                    mvc={this.state.selectedMvc}
                                    onCloseMvc={this.handleCloseMvc}
                                />
                            )}
                            showOverlay={this.state.showMvcDetails}
                        >
                            <Filters
                                dateRanges={this.state.dateRanges}
                                maxDate={this.state.filters.toDate}
                                minDate={this.state.filters.fromDate}
                                mvcTypes={dictionaries.mvc_types}
                                nearby={dictionaries.nearby}
                                offences={dictionaries.offences}
                                conditions={dictionaries.conditions}
                                participantTypes={dictionaries.mvc_participant_types}
                                onDateRangeChange={this.handleDateRangeChange}
                                onMvcTypeChange={this.handleMvcTypeChange}
                                onConditionTypeChange={this.handleConditionTypeChange}
                                onNearbyChange={this.handleNearbyChange}
                                onOffenceChange={this.handleOffenceChange}
                                onShowMap={this.handleShowMap}
                                onShowStats={this.handleShowStats}
                                onStreetChange={this.handleStreetChange}
                                onParticipantTypeChange={this.handleParticipantTypeChange}
                                onOnlyDeadChange={this.handleOnlyDeadChange}
                                onMarkersChange={this.handleMarkers}
                                selectedMvcType={filters.mvcType}
                                selectedNearby={filters.nearby}
                                selectedOffence={filters.offence}
                                selectedStreet={filters.street}
                                selectedParticipantType={filters.participantType}
                                selectedOnlyDead={filters.onlyDead}
                                selectedCondition={filters.conditionType}
                                showStats={this.state.showStats}
                                streets={this.state.streetsFromMvcs}
                            />
                        </PanelWithOverlay>
                    </div>
                </div>
            </div>
        );
    }
}

App.props = {
    areaAlias: PropTypes.string,
    cityName: PropTypes.string,
    regionAlias: PropTypes.string,
    regionLat: PropTypes.number,
    regionLon: PropTypes.number,
    regionLevel: PropTypes.number,
};
