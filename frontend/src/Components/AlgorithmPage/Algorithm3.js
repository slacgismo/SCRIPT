import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Result from "../Result/Result";
import axios from "axios";

class Algorithm3 extends Component {
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
            <div>
                <Base 
                    content={
                        <div>
                            <Content
                                text={"Scenario"}
                                compo={
                                    <Result counties={this.state.counties}     
                                    />
                                }
                            /> 
                            <br/>
                			<Content text={"Results"}/> 
                        </div>
                    }/>
            </div>
        );
    }
}

export default Algorithm3;