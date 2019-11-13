import React from "react";
import ResultChart from "./ResultChart";

function ResultCharts(props) {
    const resultCharts = props.results.map((result) => (
        <ResultChart result={ result.data } />
    ))
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;