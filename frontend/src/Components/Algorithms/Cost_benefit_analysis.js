import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario3 from "../Scenario/Scenario_cost_benefit_analysis";
import ResultCharts from "../ResultChart/ResultCharts";
import axios from "axios";

class Algorithm3 extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [], //TODO: visualize results
            profiles: []
        };
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/load_profile/")
            .then(res => {
                const profiles = res.data;
                this.setState({ profiles });
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
                                text={"Cost Benefit Analysis"}
                                compo={
                                    <Scenario3 profiles={this.state.profiles}  
                                                                     
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

export default Algorithm3;