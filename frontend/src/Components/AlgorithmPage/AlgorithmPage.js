import React, {Component} from "react";
import PropTypes from "prop-types";

import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";

import AlgInputs from "../AlgInputs/AlgInputs";
import ResultCharts from "../Result/ResultCharts";
import { dataLoadControll, dataLoadForecast } from "../Api/AlgorithmData";
import { makeStyles } from "@material-ui/core/styles";

import TextField from "@material-ui/core/TextField";

class AlgorithmPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
        };
    }

    visualizeResults(results) {
        this.setState({
            results: results,
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
                                        data={ this.props.data }
                                        algInputs={ this.props.algInputs }
                                    />
                                }
                            />
                            <br/>
                            {
                                
                                this.state.results.length > 0 &&
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
