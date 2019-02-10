export function calcRangesForDatePicker(minDate, maxDate) {
    let ranges = {};

    let currentYear = moment().year();
    for (let year = moment(minDate).year(); year <= currentYear; year++) {
        let start = moment({ year }).startOf('year');
        let end = moment({ year }).endOf('year');
        ranges[year] = [start, end];
    }

    if (minDate) {
        ranges['За всё время'] = [moment(minDate), moment(maxDate)];
    }

    return ranges;
}

export function getYearRange() {
    let currentYear = moment().year();
    return [
        moment("2018-01-01"),
        moment("2018-11-30")
    ];
}
