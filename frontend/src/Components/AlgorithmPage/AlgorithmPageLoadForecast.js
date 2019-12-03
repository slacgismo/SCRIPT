import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgorithmInputsLoadForecast from '../AlgInputs/AlgInputsLoadForecast'

function AlgorithmPageLoadForecast(props) {
    return (
        <AlgorithmPage
            title={ "Load Forecast" }
            algInputs={ AlgorithmInputsLoadForecast }
        />
    );
}

export default AlgorithmPageLoadForecast;
