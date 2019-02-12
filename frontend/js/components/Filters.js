import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import DateRangePicker from './DateRangePicker';
import FilterSelect from './FilterSelect';
import CheckBoxGroup from './CheckBoxGroup';
import CheckBox from './CheckBox';
import FileInput from './FileInput';


export default class Filters extends PureComponent {
    constructor(props) {
        super(props);

        this.loadStreetOptions = this.loadStreetOptions.bind(this);
        this.handleStreetSearchInputChange = this.handleStreetSearchInputChange.bind(this);

        this.state = {
            mvcTypeOptions: this.addNullOption(props.mvcTypes, 'Все'),
            offenceOptions: this.addNullOption(props.offences, 'Любое'),
            conditionOptions: this.addNullOption(props.conditions, 'Любое'),
            streetOptions: this.addNullOption(props.streets, 'Все'),
            nearbyOptions: this.addNullOption(props.nearby, 'Все'),
            streetSearchInput: '',
        };
    }

    componentDidUpdate(prevProps) {
        const { props } = this;

        if (props.mvcTypes !== prevProps.mvcTypes) {
            this.setState({ mvcTypeOptions: this.addNullOption(props.mvcTypes, 'Все') });
        }

        if (props.offences !== prevProps.offences) {
            this.setState({ offenceOptions: this.addNullOption(props.offences, 'Любое') });
        }

        if (props.conditions !== prevProps.conditions) {
            this.setState({ conditionOptions: this.addNullOption(props.conditions, 'Любое') });
        }

        if (props.streets !== prevProps.streets) {
            this.setState({ streetOptions: this.addNullOption(props.streets, 'Все') });
        }

        if (props.nearby !== prevProps.nearby) {
            this.setState({ nearbyOptions: this.addNullOption(props.nearby, 'Все') });
        }
    }

    addNullOption(options, name) {
        let optionsCopy = options.slice();
        optionsCopy.splice(0, 0, { id: null, name });
        return optionsCopy;
    }

    loadStreetOptions(input, callback) {
        if (!input || input.length < 3) {
            callback(null, { options: [] });
            return;
        }

        const normalizedInput = input.toLowerCase();
        let options = this.state.streetOptions.filter(
            option => option.name && option.name.toLowerCase().indexOf(normalizedInput) >= 0
        );

        callback(null, { options });
    }

    handleStreetSearchInputChange(streetSearchInput) {
        this.setState({ streetSearchInput });
    }

    getParticipantTypeParams(props) {
        let participantTypeOptions = props.participantTypes;

        const selectedParticipantTypeOption = props.selectedParticipantType;

        return { participantTypeOptions, selectedParticipantTypeOption };
    }

    getOnlyDeadOption(props){
        const selectedOnlyDeadOption = props.selectedOnlyDead;
        return { selectedOnlyDeadOption };
    }

    render() {
        const { state, props } = this;

        const selectedMvcTypeOption = state.mvcTypeOptions.find(opt => opt.id === props.selectedMvcType);
        const selectedOffenceOption = state.offenceOptions.find(opt => opt.id === props.selectedOffence);
        const selectedStreetOption = state.streetOptions.find(opt => opt.id === props.selectedStreet);
        const selectedNearbyOption = state.nearbyOptions.find(opt => opt.id === props.selectedNearby);
        const selectedConditionOption = state.conditionOptions.find(opt => opt.id === props.selectedCondition);

        const { participantTypeOptions, selectedParticipantTypeOption } = this.getParticipantTypeParams(this.props);
        const { selectedOnlyDeadOption } = this.getOnlyDeadOption(this.props);

        return (
            <div className="filters">
                <div className="d-flex justify-content-between align-items-start flex-wrap map-stats-switcher">
                    <button
                        className={'btn mr-2 mb-1' + (!this.props.showStats ? ' active' : '')}
                        onClick={this.props.onShowMap}
                    ><i
                            className={"fa fa-map-o"} aria-hidden="true">

                    </i>
                        &#160;Карта
                    </button>
                    
                    <button
                        className={'btn ' + (this.props.showStats ? ' active' : '')}
                        onClick={this.props.onShowStats}
                    ><i
                            className={"fa fa-bar-chart"} aria-hidden="true">

                    </i>
                        &#160;Статистика
                    </button>
                </div>
                
                <div className="map-legend">
                    <span>Щелкните на кружок на карте, чтобы посмотреть подробности</span>

                    <div>
                        <CheckBoxGroup
                            id="participantTypeFilter"
                            items={participantTypeOptions}
                            handleCheckboxGroupChange={this.props.onParticipantTypeChange}
                            selectedCheckBoxes={selectedParticipantTypeOption}
                        />
                    </div>
                    <div>
                        <CheckBox
                            id="onlyDeadFilter"
                            item={{id: 'onlyDead', name: 'onlyDead', label: 'только смертельные ДТП', value: selectedOnlyDeadOption}}
                            handleCheckboxChange={this.props.onOnlyDeadChange}
                        />

                    </div>

                </div>

                <div className="filter-form">
                    <div className="form-group">
                        <label htmlFor="dateFilter">
                            По дате
                        </label>

                        <DateRangePicker
                            id="dateFilter"
                            maxDate={this.props.maxDate}
                            minDate={this.props.minDate}
                            onRangeChange={this.props.onDateRangeChange}
                            ranges={this.props.dateRanges}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="typeFilter">
                            По типу
                        </label>

                        <FilterSelect
                            id="typeFilter"
                            onChange={props.onMvcTypeChange}
                            options={state.mvcTypeOptions}
                            value={selectedMvcTypeOption}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="conditionsFilter">
                            По условиям
                        </label>

                        <FilterSelect
                            id="conditionsFilter"
                            onChange={props.onConditionTypeChange}
                            options={state.conditionOptions}
                            value={selectedConditionOption}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="offenceFilter">
                            По нарушению ПДД
                        </label>

                        <FilterSelect
                            id="offenceFilter"
                            onChange={props.onOffenceChange}
                            options={state.offenceOptions}
                            value={selectedOffenceOption}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="streetFilter">
                            Улица
                        </label>

                        <FilterSelect
                            id="streetFilter"
                            loadOptions={this.loadStreetOptions}
                            noResultsText={state.streetSearchInput && state.streetSearchInput.length >= 3 ? 'Ничего не найдено' : null}
                            onChange={props.onStreetChange}
                            onInputChange={this.handleStreetSearchInputChange}
                            value={selectedStreetOption}
                        />
                    </div>

                    <div className="form-group">
                        <label htmlFor="nearbyFilter">
                            Место поблизости
                        </label>

                        <FilterSelect
                            id="nearbyFilter"
                            onChange={props.onNearbyChange}
                            options={state.nearbyOptions}
                            value={selectedNearbyOption}
                            valueKey="id"
                        />
                    </div>

                    <div className="form-group">
                        <label>
                            Загрузить маркеры на карту
                        </label>

                        <FileInput
                            attrs={{"id": "markersInput", "accept": ".txt, .json", 'class': 'form-control form-control-sm'}}
                            onChange={props.onMarkersChange}
                        />
                    </div>
                </div>
                <p className="legend-text">Координаты некоторых ДТП могут быть неточными.</p>
            </div>
        );
    }
}

Filters.props = {
    dateRanges: PropTypes.object,
    maxDate: PropTypes.string,
    minDate: PropTypes.string,
    mvcTypes: PropTypes.object.isRequired,
    nearby: PropTypes.array.isRequired,
    offences: PropTypes.object.isRequired,
    conditions: PropTypes.object.isRequired,
    participantTypes: PropTypes.array.isRequired,
    onDateRangeChange: PropTypes.func,
    onMvcTypeChange: PropTypes.func,
    onNearbyChange: PropTypes.func,
    onOffenceChange: PropTypes.func,
    onParticipantTypeChange: PropTypes.func,
    onShowMap: PropTypes.func,
    onShowStats: PropTypes.func,
    onStreetChange: PropTypes.func,
    onOnlyDeadChange: PropTypes.func,
    onConditionTypeChange: PropTypes.func,
    selectedMvcType: PropTypes.any,
    selectedNearby: PropTypes.any,
    selectedOffence: PropTypes.any,
    selectedStreet: PropTypes.any,
    selectedParticipantType: PropTypes.any,
    selectedOnlyDead: PropTypes.any,
    selectedCondition: PropTypes.any,
    showStats: PropTypes.bool,
    streets: PropTypes.object.isRequired,
};
