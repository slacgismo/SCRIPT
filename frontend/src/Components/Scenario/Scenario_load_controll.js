import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
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
        width: 250,
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

// const counties = [
//     {
//         name: "Santa Clara",
//         residents: "1",
//     },
//     {
//         name: "Santa Cruz",
//         residents: "2",
//     },
//     {
//         name: "San Francisco",
//         residents: "3",
//     },
//     {
//         name: "San Diego",
//         residents: "4",
//     },
// ];

export default function Scenario1 (props) {
    /* TODO change default parameters of Load Controll */
    const changeDefaultParameters = async () => {
    };

    const runAlgorithm = async () => {
        const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/load_controller/");
        
        let uncontrolledLoad = JSON.parse(respResults.data[0].uncontrolled_load);
        let controlledLoad = JSON.parse(respResults.data[0].controlled_load);

        console.log(uncontrolledLoad);
        console.log(controlledLoad);

        uncontrolledLoad = uncontrolledLoad.map((data, i) => (
            {
                x: i,
                y: parseFloat(data.load),
            }
        ));

        controlledLoad = controlledLoad.map((data, i) => (
            {
                x: i,
                y: parseFloat(data.load),
            }
        ));

        props.visualizeResults([{
            yAxis: "Uncontrolled Load (kWh)",
            xAxis: "Time",
            data: uncontrolledLoad,
        }, {
            yAxis: "Controlled Load (kWh)",
            xAxis: "Time",
            data: controlledLoad,
        }]);
    };
  
    const classes = useStyles();
  
    return (
        <div>
            <form noValidate autoComplete="off">
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
                    {props.counties.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))}
                </TextField>
                <br/>
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
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
                    Run
                </Button>
            </form>    
        </div>
    );
}
