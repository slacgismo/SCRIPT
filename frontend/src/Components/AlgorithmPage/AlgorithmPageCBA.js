import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgInputsCBA from '../AlgInputs/AlgInputsCBA'

// import { dataLoadControll } from "../Api/AlgorithmData";

function AlgorithmPageLoadControll(props) {
    return (
        <AlgorithmPage
            // data={ dataLoadControll }
            title={ "CBA" }
            algInputs={ AlgInputsCBA }
        />
    );
}

export default AlgorithmPageLoadControll;
