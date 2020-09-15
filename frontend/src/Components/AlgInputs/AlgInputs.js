import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import { processResults } from "../Helpers/helpers";

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
        props.visualizeResults(processResults(resultArr));
  };

    const classes = useStyles();

    const AlgInputCustomized = props.algInputs;
  
    return (
        <div>
            <form noValidate autoComplete="off">
                <AlgInputCustomized
                    category = { props.category }
                    visualizeResults={ (result) => visualizeResults(result) }
                />
            </form>    
        </div>
    );
}
