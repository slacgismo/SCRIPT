import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgorithmInputsLoadControl from '../AlgInputs/AlgInputsLoadControl'

import { dataLoadControll } from "../Api/AlgorithmData";

function AlgorithmPageLoadControll(props) {
    return (
        <AlgorithmPage
            data={ dataLoadControll }
            title={ "Load Control" }
            algInputs={ <AlgorithmInputsLoadControl /> }
        />
    );
}

export default AlgorithmPageLoadControll;
