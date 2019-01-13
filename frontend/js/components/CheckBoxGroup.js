import React, { Component } from 'react';
import PropTypes from 'prop-types';
import CheckBox from './CheckBox';

export default class CheckBoxGroup extends Component {

    constructor(props) {
        super(props);
        this.toggleCheckboxGroupChange = this.toggleCheckboxGroupChange.bind(this);
        this.setChecked = this.setChecked.bind(this);
        this.selectedCheckboxes = new Set();

        if (this.props.selectedCheckBoxes != null) {
            this.props.items.forEach(function (item) {
                if (this.props.selectedCheckBoxes.includes(item.id) === true) {
                    this.selectedCheckboxes.add(item.id)
                }
            }, this)
        }

    }

    toggleCheckboxGroupChange(item){


        if (this.selectedCheckboxes.has(item.id)) {
          this.selectedCheckboxes.delete(item.id);
        } else {

          this.selectedCheckboxes.add(item.id);

        }
        this.props.handleCheckboxGroupChange(this.selectedCheckboxes);


    }

    setChecked(item) {
        let new_item = item
        if (this.selectedCheckboxes.has(item.id)){
            new_item.value = true
        } else {
            new_item.value = false
        }
        return new_item
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

