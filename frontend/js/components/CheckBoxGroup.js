import React, {Component} from 'react';
import PropTypes from 'prop-types';
import CheckBox from './CheckBox';

export default class CheckBoxGroup extends Component {

    constructor(props) {
        super(props);
        this.toggleCheckboxGroupChange = this.toggleCheckboxGroupChange.bind(this);
        this.setChecked = this.setChecked.bind(this);
    }


    toggleCheckboxGroupChange(item) {
        let newSelectedCheckboxes = new Set(this.props.selectedCheckBoxes);
        if (newSelectedCheckboxes.has(item.id)) {
            newSelectedCheckboxes.delete(item.id);
        } else {
            newSelectedCheckboxes.add(item.id);
        }
        this.props.handleCheckboxGroupChange(newSelectedCheckboxes);
    }

    setChecked(item) {
        item.value = this.props.selectedCheckBoxes.includes(item.id)
        return item
    }


    createCheckbox(item) {
        return (
            <CheckBox
                key={"CheckBox-" + item.id}
                item={this.setChecked(item)}
                handleCheckboxChange={this.toggleCheckboxGroupChange}
            />
        );
    }

    render() {
        return (
            <div>
                {this.props.items.map(item => this.createCheckbox(item), this)}
            </div>
        );
    }
}

CheckBoxGroup.propTypes = {
    items: PropTypes.array.isRequired,
    handleCheckboxGroupChange: PropTypes.func,
    selectedCheckBoxes: PropTypes.array,
};

