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
        value: "Santa Clara",
        label: "1",
    },
    {
        value: "Santa Cruz",
        label: "2",
    },
    {
        value: "San Francisco",
        label: "3",
    },
    {
        value: "San Diego",
        label: "4",
    },
];


export default function Scenario (props) {
  
    const runAlgorithm = async () => {
        // const counties = await axios.get('http://127.0.0.1:8000/api/county');
        props.changeStatus("finished");
    };
  
    const classes = useStyles();
  
    return (
        <div>
            <form noValidate autoComplete="off">
                <TextField
                    id="standart-county"
                    select
                    label="Select your county"
                    className={classes.textField}
                    SelectProps={{
                        native: true,
                        MenuProps: {
                            className: classes.menu,
                        },
                    }}
                    margin="normal"
                >
                    {counties.map(option => (
                        <option key={option.value} value={option.value}>
                            {option.value}
                        </option>
                    ))}
                </TextField>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
            Run
                </Button>
            </form>    
        </div>
    );
}
