import React from "react";
import ResultChart from "./ResultChart";

function ResultCharts(props) {
    let resultCharts;
    if (props.algId === 1) { // Algorithm 1
        console.log("First algorithm visualized.");
        resultCharts = 
            <ResultChart
                lable_uncontrolled={ props.results[0].yAxis }
                lable_controlled={ props.results[1].yAxis}
                xAxis={ props.results[0].xAxis }
                data_uncontrolled={ props.results[0].data }
                data_controlled={ props.results[1].data}
                algId = {props.algId}
            />
        ;
    } else if (props.algId === 2) {
        console.log("Second algorithm visualized.");
        console.log(props.results);
        resultCharts = 
            <ResultChart
                results={ props.results }
                algId = { props.algId }
            />
        ;
    }
    
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;
