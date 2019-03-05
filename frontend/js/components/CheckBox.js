import React, {Component} from 'react';
import PropTypes from 'prop-types';
import {getClassByParticipantTypeName} from '../services/mvcs';

export default class CheckBox extends Component {


    constructor(props) {
        super(props);
        this.state = {
            value: this.props.item.value
        };
        this.handleInputChange = this.handleInputChange.bind(this);
    }

    handleInputChange(event) {
        const value = event.target.checked;
        let newItem = Object.assign({}, this.props.item, {value});
        this.setState({value});
        this.props.handleCheckboxChange(newItem);
    }

    render() {
        const checkboxId = "checkbox-" + this.props.item.name + this.props.item.id;
        return (
            <div className="CheckBox" id={"div-" + checkboxId}>
                <input
                    id={checkboxId}
                    key={"key-" + checkboxId}
                    type="checkbox"
                    value={this.props.item.value}
                    checked={this.props.item.value}
                    onChange={this.handleInputChange}
                />
                <label htmlFor={checkboxId} >
                <span key={"label-" + checkboxId}
                         className={"" + getClassByParticipantTypeName(this.props.item.name)}/> - {this.props.item.label}
                </label>
            </div>
        );
    }
}

CheckBox.propTypes = {
    item: PropTypes.object,
    handleCheckboxChange: PropTypes.func,
};
