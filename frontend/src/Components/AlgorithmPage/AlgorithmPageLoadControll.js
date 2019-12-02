import React from "react";
import AlgorithmPage from "./AlgorithmPage";

import { dataLoadControll } from "../Api/AlgorithmData";

function AlgorithmPageLoadControll(props) {
    return (
        <AlgorithmPage
            data={ dataLoadControll }
            title={ "Load Control" }
        />
    );
}

export default AlgorithmPageLoadControll;
