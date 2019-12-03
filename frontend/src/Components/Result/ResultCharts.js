import React from "react";
import ResultChart from "./ResultChart";

const MAX_GRAPH_PER_LINE = 3;
const FULL_WIDTH = 800;

function ResultCharts(props) {
    const graphWidth = props.results.length <= MAX_GRAPH_PER_LINE ?
        FULL_WIDTH / props.results.length :
        FULL_WIDTH / MAX_GRAPH_PER_LINE;

    const resultCharts = props.results.map((result, i) => (
        <ResultChart
            key={ i }
            results={ result }
            algId={ props.algId }
            graphWidth={ graphWidth }
            graphHeight={ graphWidth * 0.75 }
        />
    ));
    
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;
