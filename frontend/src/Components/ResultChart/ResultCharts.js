import React from "react";
import ResultChart from "./ResultChart";

function ResultCharts(props) {
    // const resultCharts = props.results.map((result) => (
    //     <ResultChart
    //         yAxis={ result.yAxis }
    //         xAxis={ result.xAxis }
    //         data={ result.data }
    //     />
    // ))
    // return (
    //     <>
    //         { resultCharts }
    //     </>
    // );

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
        console.log(props.results[2]);
        resultCharts = 
            <ResultChart
                label_r1 = { props.results[0].yAxis }
                label_r2 = { props.results[1].yAxis }
                label_rm = { props.results[2].yAxis }
                label_work={ props.results[3].yAxis }
                label_fast={ props.results[4].yAxis }
                label_p2={ props.results[5].yAxis }
                label_total={ props.results[6].yAxis}

                data_r1 = { props.results[0].data }
                data_r2 = { props.results[1].data }
                data_rm = { props.results[2].data }
                data_work={ props.results[3].data }
                data_fast={ props.results[4].data }
                data_p2={ props.results[5].data }
                data_total={ props.results[6].data}

                xAxis={ props.results[0].xAxis }
                
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