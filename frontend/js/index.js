import 'whatwg-fetch';
import React from 'react';
import ReactDOM from 'react-dom';
import App from './components/App';


function initApp(options) {
    ReactDOM.render(
        <App
            areaAlias={options.areaAlias}
            cityName={options.cityName}
            regionAlias={options.regionAlias}
            regionLat={options.regionLat}
            regionLon={options.regionLon}
            regionLevel={options.regionLevel}
        />,
        document.getElementById('react-app')
    );
}

window.initApp = initApp;
