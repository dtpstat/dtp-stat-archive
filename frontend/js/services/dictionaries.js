import { arrayToHashMap, sortByFieldAscCallback } from './utils';

export function dictionariesToHashMaps(dictionaries) {
    let asHashMaps = {};

    asHashMaps.mvc_participant_types = arrayToHashMap(dictionaries.mvc_participant_types);
    asHashMaps.mvc_types = arrayToHashMap(dictionaries.mvc_types);
    asHashMaps.offences = arrayToHashMap(dictionaries.offences);
    asHashMaps.streets = arrayToHashMap(dictionaries.streets);
    asHashMaps.nearby = arrayToHashMap(dictionaries.nearby);

    return asHashMaps;
}

export function sortDictionaries(dictionaries) {
    dictionaries.mvc_participant_types.sort(sortByFieldAscCallback('id'));
    dictionaries.mvc_types.sort(sortByFieldAscCallback('name'));
    dictionaries.offences.sort(sortByFieldAscCallback('name'));
    dictionaries.streets.sort(sortByFieldAscCallback('name'));
    dictionaries.nearby.sort(sortByFieldAscCallback('name'));
    
    return dictionaries;
}

