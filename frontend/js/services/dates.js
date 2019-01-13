export function calcRangesForDatePicker(minDate) {
    let ranges = {};

    let currentYear = moment().year();
    for (let year = currentYear - 3; year <= currentYear; year++) {
        let start = moment({ year }).startOf('year');
        let end = moment({ year }).endOf('year');
        ranges[year] = [start, end];
    }

    if (minDate) {
        ranges['За всё время'] = [moment(minDate), moment("2018-11-30")];
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
