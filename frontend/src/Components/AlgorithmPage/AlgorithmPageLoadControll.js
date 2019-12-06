import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgorithmInputsLoadControl from "../AlgInputs/AlgInputsLoadControl";

function AlgorithmPageLoadControll(props) {
    return (
        <AlgorithmPage
            title={ "Load Control" }
            algInputs={ AlgorithmInputsLoadControl }
        />
    );
}

export default AlgorithmPageLoadControll;
