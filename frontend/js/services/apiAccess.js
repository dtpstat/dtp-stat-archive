import { fetchAsJson, arrayToHashMap } from './utils';

export function getMvcs(regionAlias, areaAlias, options={}) {
    const apiUrl = areaAlias != undefined 
        ? `/api/regions/${regionAlias}/areas/${areaAlias}/mvcs/`
        : `/api/regions/${regionAlias}/mvcs/`;

    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();

        if ('onProgress' in options) {
            xhr.addEventListener('progress', options.onProgress);
        }

        xhr.addEventListener('load', () => {
            resolve(JSON.parse(xhr.responseText));
        });
        xhr.addEventListener('error', reject);

        xhr.open('GET', apiUrl);
        xhr.send();
    });
}

export function getDictionaries() {
    return fetchAsJson('/api/dicts/');
}


export function getParticipantTypes() {
    return fetchAsJson('/api/participant_types/');
}

