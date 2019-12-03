import React, {Component} from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { dataLoadControll } from "../Api/AlgorithmData";

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

const counties = [
    {
        name: "Santa Clara",
        residents: "1",
    },
    {
        name: "Santa Cruz",
        residents: "2",
    },
    {
        name: "San Francisco",
        residents: "3",
    },
    {
        name: "San Diego",
        residents: "4",
    },
];

function AlgInputsLoadControl(props) {
    const classes = useStyles();

    const getResult = () => {
        return dataLoadControll;
    }

    const runAlgorithm = async () => {
        // const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/load_forecast/");
        props.visualizeResults(getResult());
    };

    const algInputs = (
        <>
            <TextField
                id="standart-county"
                select
                className={classes.textField}
                SelectProps={{
                    native: true,
                    MenuProps: {
                        className: classes.menu,
                    },
                }}
                helperText="Please select your county"  
                margin="normal"
            >
                {
                    counties.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))
                }
            </TextField>
            <br />
            <Button
                variant="contained"
                color="primary"
                className={classes.button}
                onClick={ () => runAlgorithm() }
            >
                Run
            </Button>
        </>
    );

    return algInputs;
}

export default AlgInputsLoadControl;