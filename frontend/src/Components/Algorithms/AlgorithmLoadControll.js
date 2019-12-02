import React, {Component} from "react";
import PropTypes from "prop-types";

import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario2 from "../Result/Result";
import ResultCharts from "../Result/ResultCharts";
import { dataLoadControll, dataLoadForecast } from "../Api/AlgorithmData";

class AlgorithmLoadControll extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
        };
    }

    visualizeResults(results) {
        // Sample(Fake) result
        //
        // const resultsFake = [
        //     {
        //         yAxis: "Total Energy",
        //         xAxis: "Time",
        //         data: [
        //             {x: 1, y: 8},
        //             {x: 2, y: 10},
        //             {x: 3, y: 9},
        //             {x: 4, y: 13},
        //             {x: 5, y: 15},
        //             {x: 6, y: 10},
        //             {x: 7, y: 12},
        //             {x: 8, y: 10},
        //             {x: 9, y: 11},
        //             {x: 10, y: 12},
        //             {x: 11, y: 9},
        //             {x: 12, y: 8},
        //         ],
        //     }, {
        //         yAxis: "Total Session",
        //         xAxis: "time",
        //         data: [
        //             {x: 1, y: 8},
        //             {x: 2, y: 10},
        //             {x: 3, y: 9},
        //             {x: 4, y: 13},
        //             {x: 5, y: 15},
        //             {x: 6, y: 10},
        //             {x: 7, y: 0},
        //             {x: 8, y: 10},
        //             {x: 9, y: 11},
        //             {x: 10, y: 12},
        //             {x: 11, y: 9},
        //             {x: 12, y: 8},
        //         ],
        //     }
        // ];

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

export default AlgorithmLoadControll;
