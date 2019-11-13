import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario1 from "../Scenario/Scenario1";
import ResultCharts from "../ResultChart/ResultCharts";

class Algorithm1 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            status: "pending", // "pending" / "running" / "finished"
            results: [],
        };
    }

    changeStatus(newStatus) {
        this.setState({
            status: newStatus,
        });
    }

    visualizeResults(results) {
        const resultsFake = [
            {
                title: 'Title',
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
                title: 'Title',
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
            results: resultsFake,
            status: "finished",
        });

        console.log(this.state.results)
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
                                    <Scenario1
                                        visualizeResults={ this.visualizeResults.bind(this) }
                                    />
                                }
                            /> 
                            <br/>
                            {
                                this.state.status === "finished" &&
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