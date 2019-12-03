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

        for (const result of resultArr) {
            const data_to_visualize = {};

            for (const field of Object.keys(result)) {
                const data = result[field];
                const dataFormatted = data.map((datapoint, i) => (
                    {
                        x: i,
                        y: datapoint.load ? parseFloat(datapoint.load) : parseFloat(datapoint.data)
                    }   
                ));
                data_to_visualize[field] = {
                    yAxis: `${field}`.replace(/_/g, " "),
                    unit: "Power (kW)",
                    xAxis: "Time",  // TODO: other options?
                    data: dataFormatted,
                };
            }

            data_to_visualize_all.push(data_to_visualize);
        }

        console.log("In all charts");
        console.log(data_to_visualize_all);
        
        props.visualizeResults(data_to_visualize_all);
    };

    const classes = useStyles();

    const AlgInputCustomized = props.algInputs;
  
    return (
        <div>
            <form noValidate autoComplete="off">
                <AlgInputCustomized
                    visualizeResults={ (result) => visualizeResults(result) }
                />
            </form>    
        </div>
    );
}
