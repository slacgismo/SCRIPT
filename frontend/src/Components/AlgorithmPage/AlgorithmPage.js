import React, {Component} from "react";

import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";

import AlgInputs from "../AlgInputs/AlgInputs";
import ProgressBar from "../ProgressBar/ProgressBar";
import ResultCharts from "../Result/ResultCharts";


class AlgorithmPage extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            loading: false
        };
    }

    loadingResults(isLoading) {
        this.setState({
            loading: isLoading
        });
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
                                        controlType = { this.props.controlType }
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
                                    text={"Loading..."}
                                    compo={ <ProgressBar/> }
                                />
                            }
                            <br/>
                            {
                                this.state.results.length > 0 &&
                                this.state.loading === false &&
                                <Content
                                    text={`${ this.props.title } Results`}
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
