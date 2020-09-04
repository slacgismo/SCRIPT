import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import AlgInputsCBA from "./AlgInputsCBA";
import Button from "@material-ui/core/Button";
import axios from "axios";

const useStyles = makeStyles(theme => ({
    container: {
        display: "flex",
        flexWrap: "wrap",
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
    },
    dense: {
        marginTop: 19,
    },
    menu: {
        width: 200,
    },
    root: {
        width: 500,
        marginLeft: theme.spacing(1)
    },
    button: {
        margin: theme.spacing(1),
    },
}));

export default function AlgInputs (props) {
    const visualizeResults = (resultArr) => {
        // const result = props.data;
        const data_to_visualize_all = [];
        const isTimeSeries = resultArr[0][Object.keys(resultArr[0])[0]][0].time ? true : false; // Time or Year
        for (const result of resultArr) {
            const data_to_visualize = {};

            for (const field of Object.keys(result)) {
                const data = result[field];
                const dataFormatted = data.map((datapoint, i) => (
                    {
                        x: isTimeSeries ? i : datapoint.year,
                        y: isTimeSeries ? parseFloat(datapoint.load) : parseFloat(datapoint.data)  // option
                    }   
                ));
                data_to_visualize[field] = {
                    yAxis: `${field}`.replace(/_/g, " "),
                    unit: "Power (kW)",
                    xAxis: isTimeSeries ? "Time" : "Year",  // TODO: other options?
                    data: dataFormatted,
                };
            }

            data_to_visualize_all.push(data_to_visualize);
        }
        
        props.visualizeResults(data_to_visualize_all);
    };

    const classes = useStyles();

    const AlgInputCustomized = props.algInputs;
  
    return (
        <div>
            <form noValidate autoComplete="off">
                <AlgInputCustomized
                    category = { props.category ? props.category : null }
                    visualizeResults={ (result) => visualizeResults(result) }
                />
            </form>    
        </div>
    );
}
