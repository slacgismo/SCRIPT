import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import OverviewMap from "../OverviewMap/OverviewMap";

class Overview extends Component {
    render() {
        return (
            <div >
                <Base
                    content={
                        <Content
                            text={"Overview Map"}
                            compo={ <OverviewMap /> }
                        />
                    }
                />
            </div>
        );
    }
}

export default Overview;