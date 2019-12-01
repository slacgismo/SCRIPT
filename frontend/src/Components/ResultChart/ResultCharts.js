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
    const resultCharts = 
        <ResultChart
            lable_uncontrolled={ props.results[0].yAxis }
            lable_controlled={ props.results[1].yAxis}
            xAxis={ props.results[0].xAxis }
            data_uncontrolled={ props.results[0].data }
            data_controlled={ props.results[1].data}
        />
    ;
    return (
        <>
            { resultCharts }
        </>
    );
}

export default ResultCharts;