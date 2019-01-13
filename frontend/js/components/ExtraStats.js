import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

export default class ExtraStats extends PureComponent {
    render() {
        const mvcTypes = this.props.dictionaries.mvc_types;
        const offences = this.props.dictionaries.offences;

        return (
            <table className="extra-stats table table-borderless">
                <thead>
                    <tr>
                        <th className="mvc-types-col">По видам</th>
                        <th>По нарушениям</th>
                    </tr>
                </thead>

                <tbody>
                    <tr>
                        <td>
                            <table className="table stats-counts-list list-unstyled">
                                <tbody>
                                    {this.props.countsByMvcTypes.map(row => (
                                    <tr key={row.id}>
                                        <td className="var_name">{mvcTypes[row.id].name}</td>
                                        <td className="value">{row.count}</td>

                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </td>

                        <td>
                            <table className="table stats-counts-list list-unstyled">
                                <tbody>
                                {this.props.countsByOffences.map(row => (
                                    <tr key={row.id}>
                                        <td className="var_name"> {offences[row.id].name}</td>
                                        <td className="value">{row.count}</td>
                                    </tr>
                                ))}
                                </tbody>
                            </table>
                        </td>
                    </tr>
                </tbody>
            </table>
        );
    }
}

ExtraStats.props = {
    countsByMvcTypes: PropTypes.object,
    countsByOffences: PropTypes.object,
    dictionaries: PropTypes.object,
};
