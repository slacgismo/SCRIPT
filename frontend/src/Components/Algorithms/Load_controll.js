import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario1 from "../Scenario/Scenario_load_controll";
import ResultCharts from "../ResultChart/ResultCharts";
import axios from "axios";

class Algorithm1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
            counties: [],
        };
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/county/")
            .then(res => {
                const counties = res.data;
                this.setState({ counties });
            })
            .catch(console.log);
    }

    visualizeResults(results) {
        const resultsFake = [
            {
                yAxis: "Total Energy",
                xAxis: "Time",
                data: [
                    {x: 1, y: 8},
                    {x: 2, y: 10},
                    {x: 3, y: 9},
                    {x: 4, y: 13},
                    {x: 5, y: 15},
                    {x: 6, y: 10},
                    {x: 7, y: 12},
                    {x: 8, y: 10},
                    {x: 9, y: 11},
                    {x: 10, y: 12},
                    {x: 11, y: 9},
                    {x: 12, y: 8},
                ],
            }, {
                yAxis: "Total Session",
                xAxis: "time",
                data: [
                    {x: 1, y: 8},
                    {x: 2, y: 10},
                    {x: 3, y: 9},
                    {x: 4, y: 13},
                    {x: 5, y: 15},
                    {x: 6, y: 10},
                    {x: 7, y: 0},
                    {x: 8, y: 10},
                    {x: 9, y: 11},
                    {x: 10, y: 12},
                    {x: 11, y: 9},
                    {x: 12, y: 8},
                ],
            }
        ];

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
                                text={"Load Controll"}
                                compo={
                                    <Scenario1
                                        visualizeResults={ this.visualizeResults.bind(this)}
                                        counties={this.state.counties}
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

export default Algorithm1;