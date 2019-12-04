import React from "react";

import { ContinuousColorLegend } from "react-vis";
import { rgba } from "polished";

function OverviewMapLegend(props) {
    return (
        <ContinuousColorLegend
            style={{
                margin: "3rem",
            }}
            startTitle={ props.startValue }
            midTitle={ props.midValue }
            endTitle={ props.endValue }
            startColor={
                rgba(5, 97, 0, 0.167)
            }
            endColor={
                rgba(5, 97, 0, 1)
            }
            height={200}
            width={300}
        />
    );
}

export default OverviewMapLegend;
