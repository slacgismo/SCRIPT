import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario2 from "../Result/Result";
import ResultCharts from "../Result/ResultCharts";
import { dataLoadForecast } from "../Api/AlgorithmData";

class Algorithm2 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
        };
    }

    visualizeResults(results) {
        console.log(results === this.state.results);

        this.setState({
            results: results,
        });

        console.log(this.state.results);
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
                                    <Scenario2
                                        visualizeResults={ this.visualizeResults.bind(this) }
                                        data={ dataLoadForecast }
                                    />
                                }
                            /> 
                            <br/>
                            {
                                this.state.results.length > 0 &&
                                <Content
                                    text={"Results"}
                                    compo={
                                        <ResultCharts
                                            results={ this.state.results }
                                            algId={ 2 }
                                        />
                                    }
                                />
                            }
                        </div>
                    }
                />
            </div>
        );
    }
}

export default Algorithm2;
