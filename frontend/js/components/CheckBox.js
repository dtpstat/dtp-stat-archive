import React, { Component } from 'react';
import PropTypes from 'prop-types';
import { getClassByParticipantTypeName } from '../services/mvcs';

export default class CheckBox extends Component {


    constructor(props) {
        super(props);
        this.state = {
            checked: this.props.item.value,
            value: this.props.item.value
        };
        this.toggleCheckboxChange = this.toggleCheckboxChange.bind(this);
    }

    toggleCheckboxChange() {

        const { handleCheckboxChange,item} = this.props;
        let checkedByUser = !this.state.checked;
        let new_item = item;

        this.setState({checked: checkedByUser});
        new_item.value = checkedByUser;
        handleCheckboxChange(new_item);
    }


    render() {

        return (
            <div className="CheckBox" id={"checkbox-div-"+this.props.item.id}>
                  <input
                        id={"checkbox-"+this.props.item.id}
                        key={"checkbox-key-"+this.props.item.id}
                        type="checkbox"
                        value={this.props.item.value}
                        checked={this.state.checked}
                        onChange={this.toggleCheckboxChange}
                  /> <span key={"checkbox-label-"+this.props.item.id} className={"" + getClassByParticipantTypeName(this.props.item.name)}/> - {this.props.item.label}
            </div>
        );
    }
}

CheckBox.propTypes = {
    item: PropTypes.object,
    handleCheckboxChange: PropTypes.func,
};
