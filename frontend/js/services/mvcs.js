import { sortByFieldAscCallback } from './utils';

const colorsByParticipantTypes = {
    'auto': '#FFCC66',
    'pedestrian': '#99CCFF',
    'bicycle': '#99CC99'
};


const classByParticipantName = {
    'auto': 'legend-circle color-auto',
    'pedestrian': 'legend-circle color-pedestrian',
    'bicycle': 'legend-circle color-bicycle',
    'onlyDead': 'fa fa-circle-o',
};

export function getColorByParticipantTypeId(participantTypeId, participantTypes) {
        const typeName = participantTypes[participantTypeId].name;
        return colorsByParticipantTypes[typeName];

}

export function getClassByParticipantTypeName(participantTypeName) {

        return classByParticipantName[participantTypeName];
}

export function getStreetsFromMvcs(mvcs, streets) {
    let streetsFromMvcs = {};
    mvcs.forEach((mvc) => {
        if (mvc.street != undefined) {
            streetsFromMvcs[mvc.street] = streets[mvc.street];
        }
    });
    return Object.values(streetsFromMvcs).sort(sortByFieldAscCallback('name'));
}

export function filterMvcs(mvcs, mvcFilters) {

    let filters = Object.assign({}, mvcFilters, {
        fromDate: mvcFilters.fromDate && mvcFilters.fromDate.toISOString(),
        toDate: mvcFilters.toDate && mvcFilters.toDate.toISOString(),
    });

    return mvcs.filter(mvc => isMvcFiltered(mvc, filters));
}

export function getMinMaxDates(mvcs) {
    if (mvcs.length === 0) {
        return { minDate: null, maxDate: null };
    }

    let minDate = mvcs[0].datetime;
    let maxDate = mvcs[0].datetime;

    for (let i = 1; i < mvcs.length; i++) {
        let mvc = mvcs[i];
        if (mvc.datetime < minDate) {
            minDate = mvc.datetime;
        }
        if (mvc.datetime > maxDate) {
            maxDate = mvc.datetime;
        }
    }

    minDate = new Date(minDate);
    maxDate = new Date(maxDate);

    return { minDate, maxDate };
}

export function getMvcTypeName(mvc, dictionaries) {
    let mvcType = dictionaries.mvc_types[mvc.type_id];
    return mvcType.name;
}



export function mvcHasDeadParticipants(mvc) {
    return mvc.participants.some(p => p.dead);
}

export function getMiddleCoord(mvcs) {
    let latitude = 0, longitude = 0;

    for (let i = 0; i < mvcs.length; i++) {
        latitude += mvcs[i].latitude / mvcs.length;
        longitude += mvcs[i].longitude / mvcs.length;
    }

    return { latitude, longitude };
}

function isMvcFiltered(mvc, mvcFilters) {


    if (mvcFilters.mvcType) {
        if (mvc.type_id !== mvcFilters.mvcType) {
            return false;
        }
    }

    if (mvcFilters.nearby) {
        if (!mvc.nearby.includes(mvcFilters.nearby)) {
            return false;
        }
    }

    if (mvcFilters.offence) {
        if (!mvcHasOffence(mvc, mvcFilters.offence)) {
            return false;
        }
    }

    if (mvcFilters.street) {
        if (mvc.street !== mvcFilters.street) {
            return false;
        }
    }

    if (mvcFilters.participantType) {
        if (mvcFilters.participantType.includes(mvc.participant_type_id) === false ) {
            return false;
        }
    }

    if (mvcFilters.onlyDead) {
        if (mvc.dead === 0) {
            return false;
        }
    }

    if (mvcFilters.conditionType) {
        if (mvcFilters.conditionType === 1 && mvc.conditions.includes("Светлое время суток")) {
            return false;
        }
        if (mvcFilters.conditionType === 2 && !mvc.conditions.includes("Светлое время суток")) {
            return false;
        }
    }

    if (mvcFilters.fromDate && mvcFilters.toDate) {
        if (mvcFilters.fromDate > mvc.datetime ||
            mvcFilters.toDate < mvc.datetime
        ) {
            return false;
        }
    }

    return true;
}

function mvcHasOffence(mvc, offenceId) {
    for (let i = 0; i < mvc.participants.length; i++) {
        let participant = mvc.participants[i];
        for (let j = 0; j < participant.offences.length; j++) {
            if (participant.offences[j] === offenceId) {
                return true;
            }
        }
    }

    return false;
}
