import React, { Component } from 'react';
import PropTypes from 'prop-types';

const localeOptions = {
    "format": "DD.MM.YYYY",
    "separator": " - ",
    "applyLabel": "Применить",
    "cancelLabel": "Отмена",
    "fromLabel": "От",
    "toLabel": "До",
    "customRangeLabel": "Выбрать",
    "weekLabel": "Нед",
    "daysOfWeek": [
        "Вс",
        "Пн",
        "Вт",
        "Ср",
        "Чт",
        "Пт",
        "Сб"
    ],
    "monthNames": [
        "Январь",
        "Февраль",
        "Март",
        "Апрель",
        "Май",
        "Июнь",
        "Июль",
        "Август",
        "Сентябрь",
        "Октябрь",
        "Ноябрь",
        "Декабрь"
    ],
    "firstDay": 1
};

export default class DateRangePicker extends Component {
    constructor(props) {
        super(props);

        this.setRef = this.setRef.bind(this);
    }

    componentDidMount() {
        this.$input = $(this.input);

        this.$input.daterangepicker({
            startDate: this.props.minDate,
            endDate: this.props.maxDate,
            opens: 'left',
            locale: localeOptions,
            ranges: this.props.ranges,
            alwaysShowCalendars: true,
            showCustomRangeLabel: false,
        }, (start, end, label) => {
            this.props.onRangeChange && this.props.onRangeChange(start, end);
        });
    }

    setRef(input) {
        this.input = input;
    }

    render() {
        return (
            <input
                className="form-control date-filter"
                id={this.props.id}
                ref={this.setRef}
                type="text"
            />
        )
    }
}

DateRangePicker.propTypes = {
    id: PropTypes.string,
    maxDate: PropTypes.object,
    minDate: PropTypes.object,
    onRangeChange: PropTypes.func,
    ranges: PropTypes.object,
};
