import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

export default class BriefStats extends PureComponent {
    render() {
        return (
            <div className="brief-stats">
                <table className="table table-borderless">
                    <tbody>
                        <tr>
                            <td className="city-name align-middle"> </td>
                            <td className="align-middle text-center">Пострадавшие <b>{this.props.injured}</b></td>
                            <td className="align-middle text-center">Погибшие <b>{this.props.dead}</b></td>
                        </tr>

                        <tr>
                            <td>
                                <span className="align-middle">Количество ДТП</span>
                                <span className="mvc-count ml-2 align-middle">
                                    {this.props.mvcCount}
                                </span>
                            </td>

                            <td>
                                <div className="row justify-content-center">
                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/driver.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.injuredAuto}
                                        </div>
                                    </div>
                                    
                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/pedestrian.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.injuredPedestrian}
                                        </div>
                                    </div>

                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/cyclist.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.injuredBicycle}
                                        </div>
                                    </div>
                                </div>
                            </td>

                            <td>
                                <div className="row justify-content-center">
                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/driver.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.deadAuto}
                                        </div>
                                    </div>
                                    
                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/pedestrian.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.deadPedestrian}
                                        </div>
                                    </div>

                                    <div className="col-auto media align-items-center">
                                        <img
                                            src={"/static/media/cyclist.png"}
                                        />

                                        <div className="media-body">
                                            {this.props.deadBicycle}
                                        </div>
                                    </div>
                                </div>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        );
    }
}

BriefStats.props = {
    cityName: PropTypes.string,
    dead: PropTypes.number,
    deadAuto: PropTypes.number,
    deadBicycle: PropTypes.number,
    deadPedestrian: PropTypes.number,
    injured: PropTypes.number,
    injuredAuto: PropTypes.number,
    injuredBicycle: PropTypes.number,
    injuredPedestrian: PropTypes.number,
    mvcCount: PropTypes.number,
};
