import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import Scenario from "./Scenario";

class Algorithm4 extends Component {
    render() {
        return (
            <div >
                <Base 
                    content={
                        <div>
                            <Content text={"Scenario"} compo={<Scenario />}/> 
                            <br/>
                            <Content text={"Results"}/>        
                        </div>
                    }/>
            </div>
        );
    }
}

export default Algorithm4;