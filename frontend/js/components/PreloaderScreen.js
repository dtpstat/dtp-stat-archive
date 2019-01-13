import React from 'react';

const PreloaderScreen = (props) => (
    <div className="preloader-screen">
        <div className="preloader-wrapper">
            <div className="preloader-header">
                Загрузка...
            </div>

            <div className="preloader">
                <i className="preloader-icon fa fa-spinner" />
            </div>
        </div>
    </div>
)

export default PreloaderScreen;
