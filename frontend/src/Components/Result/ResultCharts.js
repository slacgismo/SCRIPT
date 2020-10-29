import React from "react";
import ResultChart from "./ResultChart";

const MAX_GRAPH_PER_LINE = 3;
const FULL_WIDTH = 800;

export function ResultCharts(props) {
    const graphWidth = props.results.length <= MAX_GRAPH_PER_LINE ?
        FULL_WIDTH / props.results.length :
        FULL_WIDTH / MAX_GRAPH_PER_LINE ;
    
    // If no results, no legend is needed.
    const legendPosition = !props.results.length ? "none" : "right";

    const resultCharts = props.results.map((result, i) => (
        <ResultChart
            key={ i }
            results={ result }
            subtitle={}
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
