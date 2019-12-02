import React from "react";
import ResultChart from "./ResultChart";

function ResultCharts(props) {
    const resultCharts = props.results.map((result, i) => (
        <ResultChart
            key={ i }
            results={ result }
            algId = { props.algId }
        />
    ));
    
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;
