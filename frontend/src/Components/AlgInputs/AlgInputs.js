import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { processResults } from "../Helpers/Helpers";

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


    const visualizeResults = (resultArr, isCBA) => {
        props.visualizeResults(processResults(resultArr, isCBA));
    };

    const classes = useStyles();

    const AlgInputCustomized = props.algInputs;
  
    return (
        <div>
            <form noValidate autoComplete="off">
                <AlgInputCustomized
                    category = { props.category }
                    controlType = {props.controlType }
                    visualizeResults={ (result, isCBA) => visualizeResults(result, isCBA) }
                    setChartTitles={ (chartTitles) => props.setChartTitles(chartTitles) }
                    checkCBA={ (isCBA) => props.checkCBA(isCBA) }
                    loadingResults={ (isLoading) => props.loadingResults(isLoading)}
                />
            </form>    
        </div>
    );
}
