// Fetch basic data
//
// axios('http://127.0.0.1:8000/api/county/')
// .then(res => {
//     const counties = res.data
//     console.log(counties)
//     this.setState({ counties })
//     console.log(this.state.counties)
// })
// .catch(console.log)
import axios from "axios";
import React, {Component} from "react";
import AlgInputsLoadControl from "../AlgInputs/AlgInputsLoadControl"

class BasicData extends Component {
    state = {
        counties: []
    }

    componentDidMount() {
        axios('http://127.0.0.1:8000/api/county/')
        .then(res => {
            const counties = res.data
            console.log(counties)
            this.setState({ counties })
            console.log(this.state.counties)
        })
        .catch(console.log)
    }

    render() {
        return (
        <AlgInputsLoadControl counties={this.state.counties} />
        );
    }
}

export default BasicData;