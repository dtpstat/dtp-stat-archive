import React, { PureComponent } from 'react';
import PropTypes from 'prop-types';

export default class PanelWithOverlay extends PureComponent {
    constructor(props) {
        super(props);

        this.setOverlayRef = this.setOverlayRef.bind(this);
        this.setMainContentAreaRef = this.setMainContentAreaRef.bind(this);
    }

    componentDidUpdate(prevProps) {
        if (!prevProps.showOverlay && this.props.showOverlay) {
            this.$overlay.animate({ right: '+=100%' });
            this.$mainContentArea.hide();
        } else if (prevProps.showOverlay && !this.props.showOverlay) {
            this.$overlay.animate({ right: '-=100%' });
            this.$mainContentArea.show();
        }
    }

    setOverlayRef(overlay) {
        this.overlay = overlay;
        this.$overlay = $(overlay);
    }

    setMainContentAreaRef(mainContentArea) {
        this.mainContentArea = mainContentArea;
        this.$mainContentArea = $(mainContentArea);
    }

    render() {
        return (
            <div className="panel-with-overlay">
                <div
                    className="main-content-area"
                    ref={this.setMainContentAreaRef}
                >
                    {this.props.children}
                </div>

                <div 
                    className="overlay-area"
                    ref={this.setOverlayRef}
                >
                    {this.props.overlay}
                </div>
            </div>
        );
    }
}

PanelWithOverlay.props = {
    children: PropTypes.node,
    overlay: PropTypes.node,
    showOverlay: PropTypes.bool,
};
