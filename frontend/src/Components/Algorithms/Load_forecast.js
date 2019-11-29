import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario2 from "../Scenario/Scenario_load_forecast";
import ResultCharts from "../ResultChart/ResultCharts";
import axios from "axios";

class Algorithm2 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [], //TODO: visualize results
            counties: []
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

    render() {
        return (
            <div>
                <Base 
                    content={
                        <div>
                            <Content
                                text={"Load Forecast"}
                                compo={
                                    <Scenario2 counties={this.state.counties}     
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

export default Algorithm2;