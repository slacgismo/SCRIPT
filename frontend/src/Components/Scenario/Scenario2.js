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

export default function Scenario2 (props) {
    const runAlgorithm = async () => {
        const respResults = await axios.get("http://localhost:8000/api/algorithm/load_forecast/");

        console.log(respResults.data)
        console.log(JSON.parse(respResults))

        // props.visualizeResults([{
        //   yAxis: 'Uncontrolled Load (kWh)',
        //   xAxis: 'Time',
        //   data: uncontrolledLoad,
        // }, {
        //   yAxis: 'Controlled Load (kWh)',
        //   xAxis: 'Time',
        //   data: controlledLoad,
        // }])
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
                    helperText="Please select your county"
                    margin="normal"
                >
                    {props.counties.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))}
                </TextField>
                <p/>
                <Button variant="contained" color="primary"  >
                    Run
                </Button>
            </form>    
        </div>
    );
}
