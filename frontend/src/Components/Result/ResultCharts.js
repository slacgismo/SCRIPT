import React from "react";
import ResultChart from "./ResultChart";

const MAX_GRAPH_PER_LINE = 3;
const FULL_WIDTH = 800;

function ResultCharts(props) {
    const graphWidth = props.results.length <= MAX_GRAPH_PER_LINE ?
        FULL_WIDTH / props.results.length :
        FULL_WIDTH / MAX_GRAPH_PER_LINE ;
    
    // If only one line, it should be enough to use title only, so no legend is needed.
    const legendPosition = Object.keys(props.results[0]).length === 1 ? "none" : "right";

    const resultCharts = props.results.map((result, i) => (
        <ResultChart
            key={ i }
            results={ result }
            algId={ props.algId }
            graphWidth={ 400 }
            graphHeight={ 300 }
            legendPosition={ legendPosition }
        />
    ));
    
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;
