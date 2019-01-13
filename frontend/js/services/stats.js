import { participantRoles } from './consts';
import { sortByFieldDescCallback } from './utils';

export function calcInjuredAndDeadCounts(mvcs) {
    let injured = 0, injuredAuto = 0, injuredPedestrian = 0, injuredBicycle = 0;
    let dead = 0, deadAuto = 0, deadPedestrian = 0, deadBicycle = 0;

    mvcs.forEach((mvc) => {
        injured += mvc.injured;
        dead += mvc.dead;

        mvc.participants.forEach((participant) => {
            switch (participant.role) {
                case participantRoles.auto:
                    if (participant.injured) {
                        injuredAuto++;
                    } else if (participant.dead) {
                        deadAuto++;
                    }
                    break;

                case participantRoles.pedestrian:
                    if (participant.injured) {
                        injuredPedestrian++;
                    } else if (participant.dead) {
                        deadPedestrian++;
                    }
                    break;

                case participantRoles.bicycle:
                    if (participant.injured) {
                        injuredBicycle++;
                    } else if (participant.dead) {
                        deadBicycle++;
                    }
                    break;
            }
        });
    });

    return {
        dead,
        deadAuto,
        deadBicycle,
        deadPedestrian,
        injured,
        injuredAuto,
        injuredBicycle,
        injuredPedestrian,
    };
}

export function calcCountsByMvcTypes(mvcs, dictionaries) {
    let countsByMvcTypes = {};
    dictionaries.mvc_types.forEach((mvcType) => {
        countsByMvcTypes[mvcType.id] = 0;
    });

    mvcs.forEach((mvc) => {
        countsByMvcTypes[mvc.type_id]++;
    });

    let flatList = Object.keys(countsByMvcTypes).map(mvcTypeId => ({
        id: Number(mvcTypeId),
        count: countsByMvcTypes[mvcTypeId],
    }));

    flatList = flatList.filter(item => item.count > 0);
    flatList = flatList.sort(sortByFieldDescCallback('count'));

    return flatList;
}

export function calcCountsByOffences(mvcs, dictionaries) {
    let countsByOffences = {};
    dictionaries.offences.forEach((offence) => {
        countsByOffences[offence.id] = 0;
    });

    mvcs.forEach((mvc) => {
        mvc.participants.forEach((participant) => {
            participant.offences.forEach((offenceId) => {
                countsByOffences[offenceId]++;
            });
        });
    });

    let flatList = Object.keys(countsByOffences).map(offenceId => ({
        id: Number(offenceId),
        count: countsByOffences[offenceId],
    }));

    flatList = flatList.filter(item => item.count > 0);
    flatList = flatList.sort(sortByFieldDescCallback('count'));

    return flatList;
}
