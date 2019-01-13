import React, { Component } from 'react';
import PropTypes from 'prop-types';
import Select, { Async } from 'react-select';

const scrollPadding = 5;

export default class FilterSelect extends Component {
    constructor(props) {
        super(props);

        this.handleOpen = this.handleOpen.bind(this);
        this.handleInputChange = this.handleInputChange.bind(this);

        this.wrapperRef = React.createRef();
    }

    scrollToMenu() {
        const wrapper = this.wrapperRef.current;
        const withScroll = this.findAncestorWithScroll(wrapper);

        if (withScroll) {
            let $withScroll = $(withScroll);
            let $menu = $(wrapper).find('.Select-menu-outer');
            if ($menu.length === 0) {
                return;
            }

            let top = this.topRelativeTo($menu, withScroll);
            let menuBottom = top + $menu.height();
            let scrollTop = menuBottom - withScroll.clientHeight + scrollPadding;
            if (scrollTop > $withScroll.scrollTop()) {
                $withScroll.scrollTop(scrollTop);
            }
        }
    }

    findAncestorWithScroll(element) {
        let current = element.parentElement;
        while (current !== null) {
            if (current.scrollHeight > current.clientHeight && $(current).css('overflow-y') === 'auto') {
                return current;
            }
            current = current.parentElement;
        }
        return null;
    }

    topRelativeTo($element, ancestor) {
        const root = $('html')[0];
        let top = 0;
        while (true) {
            top += $element.position().top;

            let offsetParent = $element.offsetParent()[0];
            if (offsetParent === ancestor || offsetParent === root) {
                return top + $(ancestor).scrollTop();
            }

            $element = $element.offsetParent();
        }
    }

    handleOpen() {
        setTimeout(() => this.scrollToMenu(), 0);
    }

    handleInputChange(input) {
        this.props.onInputChange && this.props.onInputChange(input);

        setTimeout(() => this.scrollToMenu(), 0);
    }

    render() {
        const { props } = this;

        const SelectComponent = 'loadOptions' in props ? Async : Select;

        return (
            <div
                className="filter-select"
                ref={this.wrapperRef}
            >
                <SelectComponent
                    clearable={true}
                    clearValueText="Очистить"
                    id={props.id}
                    labelKey="name"
                    loadOptions={props.loadOptions}
                    noResultsText={props.noResultsText === undefined ? 'Ничего не найдено' : props.noResultsText}
                    onChange={props.onChange}
                    onInputChange={this.handleInputChange}
                    onOpen={this.handleOpen}
                    options={props.options}
                    searchable={true}
                    searchPromptText="Начните печатать для поиска"
                    value={props.value}
                    valueKey="id"
                />
            </div>
        )
    }
}

FilterSelect.propTypes = {
    id: PropTypes.string,
    loadOptions: PropTypes.func,
    noResultsText: PropTypes.string,
    onChange: PropTypes.func,
    onInputChange: PropTypes.func,
    options: PropTypes.array,
    value: PropTypes.object,
};
