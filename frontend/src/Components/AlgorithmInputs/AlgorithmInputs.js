import React from 'react';
import Content from "../../Layouts/Content";
import AlgResult from "../Result/Result";

function AlgorithmInputs(props) {
    return (
        <Content
            text={`${ props.title } Inputs`}
            compo={
                <AlgResult
                    visualizeResults={ props.visualizeResults.bind(this) }
                    data={ props.data }
                />
            }
        />
    )
}

export default AlgorithmInputs;