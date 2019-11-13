import React from "react";
import ResultChart from "./ResultChart";

function ResultCharts(props) {
    const resultCharts = props.results.map((result) => (
        <ResultChart
            yAxis={ result.yAxis }
            xAxis={ result.xAxis }
            data={ result.data }
        />
    ))
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;