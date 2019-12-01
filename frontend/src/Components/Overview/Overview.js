import React, {Component} from "react";
import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";
import OverviewMap from "../OverviewMap/OverviewMap";
import OverviewMapTabs from '../OverviewMap/OverviewMapTabs'

class Overview extends Component {
    render() {
        return (
            <div >
                <Base
                    content={
                        <OverviewMap />
                        // <Content
                        //     text={"Overview Map"}
                        //     compo={
                        //         <OverviewMap overviewParam={"totalEnergy"}/>
                        //     }
                        // />
                    }
                />
            </div>
        );
    }
}

export default Overview;