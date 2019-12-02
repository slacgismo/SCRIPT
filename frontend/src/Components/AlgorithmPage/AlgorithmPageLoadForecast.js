import React from "react";
import AlgorithmPage from "./AlgorithmPage";

import { dataLoadForecast } from "../Api/AlgorithmData";

function AlgorithmPageLoadForecast(props) {
    return (
        <AlgorithmPage
            data={ dataLoadForecast }
        />
    );
}

export default AlgorithmPageLoadForecast;
