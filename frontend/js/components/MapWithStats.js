import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Map from './Map';
import BriefStats from './BriefStats';
import ExtraStats from './ExtraStats';

export default class MapWithStats extends Component {
    constructor(props) {
        super(props);

        this.setMapCollapseRef = this.setMapCollapseRef.bind(this);
        this.setExtraStatsRef = this.setExtraStatsRef.bind(this);
    }

    componentDidUpdate(prevProps) {
        if (prevProps.showStats && !this.props.showStats) {
            this.$extraStats.removeClass('flex-grow-1');
            this.$mapCollapse.addClass('flex-grow-1');
            this.$mapCollapse.collapse('show');
        } else if (!prevProps.showStats && this.props.showStats) {
            this.$mapCollapse.removeClass('flex-grow-1');
            this.$extraStats.addClass('flex-grow-1');
            this.$extraStats.collapse('show');
        }
    }

    setMapCollapseRef(mapCollapse) {
        this.mapCollapse = mapCollapse;
        this.$mapCollapse = $(mapCollapse);
    }

    setExtraStatsRef(extraStats) {
        this.extraStats = extraStats;
        this.$extraStats = $(extraStats);
    }

    getToggleStatsButtonClass() {
        let arrowClass = this.props.showStats ? 'fa-angle-down' : 'fa-angle-up';
        return `fa ${arrowClass}`;
    }

    render() {
        const stats = this.props.stats;

        return (
            <div className="map-with-stats d-flex flex-column">
                <div
                    className="map-section collapse show flex-grow-1"
                    data-parent=".map-with-stats"
                    ref={this.setMapCollapseRef}
                >
                    <Map
                        defaultCoord={this.props.defaultCoord}
                        searchParams={this.props.searchParams}
                        dictionaries={this.props.dictionaries}
                        mvcs={this.props.mvcs}
                        mapObjectsMarkersData={this.props.mapObjectsMarkersData}
                        onMvcSelected={this.props.onMvcSelected}
                        onMapChanges={this.props.onMapChanges}
                        regionLevel={this.props.regionLevel}
                    />
                </div>

                <div className="brief-stats-section">
                    <div className="text-center">
                        <button
                            className="btn toggle-stats-btn"
                            onClick={this.props.onToggleStats}
                        >
                            <i className={this.getToggleStatsButtonClass()} />
                        </button>
                    </div>

                    <BriefStats
                        cityName={this.props.cityName}
                        dead={stats.dead}
                        deadAuto={stats.deadAuto}
                        deadBicycle={stats.deadBicycle}
                        deadPedestrian={stats.deadPedestrian}
                        injured={stats.injured}
                        injuredAuto={stats.injuredAuto}
                        injuredBicycle={stats.injuredBicycle}
                        injuredPedestrian={stats.injuredPedestrian}
                        mvcCount={stats.mvcCount}
                    />
                </div>

                <div
                    className="extra-stats-section collapse flex-grow-1"
                    data-parent=".map-with-stats"
                    ref={this.setExtraStatsRef}
                >
                    <ExtraStats
                        countsByMvcTypes={stats.countsByMvcTypes}
                        countsByOffences={stats.countsByOffences}
                        dictionaries={this.props.dictionaries}
                    />
                </div>
            </div>
        );
    }
}

MapWithStats.props = {
    cityName: PropTypes.string,
    defaultCoord: PropTypes.object,
    searchParams: PropTypes.object,
    dictionaries: PropTypes.object,
    mvcs: PropTypes.array,
    onMvcSelected: PropTypes.func,
    onMapChanges: PropTypes.func,
    onToggleStats: PropTypes.func,
    regionLevel: PropTypes.number,
    showStats: PropTypes.bool,
    stats: PropTypes.object,    
};
