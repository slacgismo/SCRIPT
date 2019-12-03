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

    /* TODO change default parameters of Load Controll */
    const changeDefaultParameters = async () => {
    };

    const getResult = () => {
        return dataLoadControll;
    };

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
                helperText="Please select a county"  
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
            <Button variant="contained" className={classes.button} onClick={changeDefaultParameters}>
                    Default parameters
            </Button>
            <br/>
            <TextField
                disabled
                id="standard-rate_energy_peak"
                label="rate_energy_peak"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
            <TextField
                disabled
                id="standard-rate_energy_partpeak"
                label="rate_energy_partpeak"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
            <TextField
                disabled
                id="standard-rate_energy_offpeak"
                label="rate_energy_offpeak"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
            <TextField
                disabled
                id="standard-rate_demand_peak"
                label="rate_demand_peak"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
            <TextField
                disabled
                id="standard-rate_demand_partpeak"
                label="rate_demand_partpeak"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
            <TextField
                disabled
                id="standard-rate_demand_overall"
                label="rate_demand_overall"
                defaultValue="defaulValue"
                className={classes.textField}
                margin="normal"
            />
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
