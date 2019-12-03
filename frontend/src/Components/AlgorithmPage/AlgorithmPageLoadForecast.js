import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgorithmInputsLoadForecast from '../AlgInputs/AlgInputsLoadForecast'
import { dataLoadForecast } from "../Api/AlgorithmData";

function AlgorithmPageLoadForecast(props) {
    return (
        <AlgorithmPage
            data={ dataLoadForecast }
            title={ "Load Forecast" }
            algInputs={ <AlgorithmInputsLoadForecast /> }
        />
    );
}

export default AlgorithmPageLoadForecast;
