export function fetchAsJson(url) {
	return fetch(url).then((response) => {
		return response.json();
	});
}

export function arrayToHashMap(array, keyField = 'id', valueField = null) {
    return array.reduce((obj, element) => {
        obj[element[keyField]] = valueField ? element[valueField] : element;
        return obj;
    }, {});
}

export const sortByFieldAscCallback = (fieldName) => (a, b) => {
    if (a[fieldName] < b[fieldName]) {
        return -1;
    } else if (a[fieldName] > b[fieldName]) {
        return 1;
    } else {
        return 0;
    }
}

export const sortByFieldDescCallback = (fieldName) => (a, b) => {
    if (a[fieldName] < b[fieldName]) {
        return 1;
    } else if (a[fieldName] > b[fieldName]) {
        return -1;
    } else {
        return 0;
    }
}
