import React, { Component } from 'react';


export default class FileInput extends Component {

    constructor(props) {
        super(props);
        this.readFile = this.readFile.bind(this);
    }

    readFile(file){
        let reader = new FileReader();
        reader.onloadend = () =>{
            let markers = JSON.parse(reader.result);
            this.props.onChange(markers);
        };
        reader.readAsText(file.target.files[0]);
    };

    render() {
        const {attrs} = this.props;

        return (
            <div id={"file-"+ attrs.id}>
                  <input className={attrs.class}
                        id={"file-"+attrs.id}
                        key={"file-key-"+attrs.id}
                        accept={attrs.accept}
                        type="file"
                        onChange={this.readFile}
                  />
            </div>
        );
    }
}

// FileInput.propTypes = {
//     item: PropTypes.object,
//     handleCheckboxChange: PropTypes.func,
// };
