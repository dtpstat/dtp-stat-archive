import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';
import { getMvcTypeName } from '../services/mvcs';
import { getParticipantsWithOffences } from '../services/participants';
import { participantRoles } from '../services/consts';

export default class MvcDetails extends PureComponent {
    getParticipantIconClass(role) {
        switch (role) {
            case participantRoles.auto:
                return 'fa-car';
            case participantRoles.pedestrian:
                return 'fa-male';
            case participantRoles.bicycle:
                return 'fa-bicycle';
            default:
                return '';
        }
    }

    render() {
        const mvc = this.props.mvc;

        if (!mvc) {
            return null;
        }

        const dictionaries = this.props.dictionaries;
        const date = moment(mvc.datetime);

        const participantsWithOffences = getParticipantsWithOffences(mvc.participants, dictionaries);   

        return (
            <div className="mvc-details">
                <button
                    aria-label="Close"
                    className="close"
                    onClick={this.props.onCloseMvc}
                    type="button"
                >
                    <span aria-hidden="true">&times;</span>
                </button>

                <h4>
                    {date.format('DD.MM.YYYY')}
                </h4>

                <h5>
                    {getMvcTypeName(mvc, dictionaries)}
                </h5>

                <p>
                    Пострадали - {mvc.injured}, погибли - {mvc.dead}
                </p>



                <div>
                    <p className="list-header">
                        Нарушения:
                    </p>

                    <ul className="offence-list list-unstyled">
                        {participantsWithOffences.map((po, index) => (
                            <li
                                className="media align-items-center"
                                key={index}
                            >
                                <i
                                    className={'mr-3 fa ' + this.getParticipantIconClass(po.role)}
                                    aria-hidden="true"
                                />
                                <div className="media-body">
                                    {po.offenceName}
                                </div>
                            </li>
                        ))}
                    </ul>
                </div>

                <div className="text-center">
                    <a
                        className="more-link btn btn-outline-dark"
                        href={"/dtp/" + mvc.alias}
                        target="_blank"
                    >
                        Подробнее
                    </a>
                </div>
            </div>
        );
    }
}

MvcDetails.props = {
    dictionaries: PropTypes.object,
    mvc: PropTypes.object,
    onCloseMvc: PropTypes.func,
};
