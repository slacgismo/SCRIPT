import React, {Component} from "react";
import PropTypes from "prop-types";

import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";

import AlgInputs from "../AlgInputs/AlgInputs";
import ProgressBar from "../ProgressBar/ProgressBar";
import ResultCharts from "../Result/ResultCharts";
import { dataLoadControll, dataLoadForecast } from "../Api/AlgorithmData";
import { makeStyles } from "@material-ui/core/styles";

import TextField from "@material-ui/core/TextField";
import axios from "axios";

class AlgorithmPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            loading: false
        };
    }

    loadingResults = async() => {
        this.setState({
            loading: true
        })
        const res = await axios({
            url: "http://127.0.0.1:8000/api/check_algorithm_runner_status",
            method: "post",
            data: {task_name:  "script.tasks.run_cba_tool"}
        });
        if (res['data']===false){
            this.setState({
                loading: false
            })
        }
    }


    visualizeResults(results) {
        this.setState({
            results: results
        });
    }

    render() {
        return (
            <div>
                <Base 
                    content={
                        <div>
                            <Content
                                text={`${ this.props.title } Inputs`}
                                compo={
                                    <AlgInputs
                                        category={ this.props.categoryProp }
                                        title={ this.props.title }
                                        visualizeResults={ this.visualizeResults.bind(this) }
                                        loadingResults={ this.loadingResults.bind(this) }
                                        algInputs={ this.props.algInputs }
                                    />
                                }
                            />
                            <br/>
                            {   this.state.loading === true &&
                                <Content
                                    text={`Loading...`}
                                    compo={ <ProgressBar/> }
                                />
                            }
                            <br/>
                            {
                                this.state.results.length > 0 &&
                                this.state.loading === false &&
                                <Content
                                    text={`${ this.props.title } Results`}
                                    // 
                                    textField = {this.props.compo}
                                    compo={
                                        
                                        <ResultCharts
                                            results={ this.state.results }
                                            algId={2}
                                        />
                                    }
                                />
                            }
                        </div>
                    }/>
            </div>
        );
    }
}

export default AlgorithmPage;
