import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import axios from "axios";
import { dataLoadForecast } from "../Api/AlgorithmData";

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

function AlgInputsLoadForecast (props) {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);

    const handleClose = () => {
        setOpen(false);
    };

    /* TODO save results(profile) of Load Forecast*/
    const saveResults = () => {
        setOpen(false);
        // TODO: backend
        // POST data to save as a profile
    };

    // TODO: backend
    const getResult = () => {
        const dataLoadForecast = axios.get("http://127.0.0.1:8000/api/algorithm/load_forecast/");
        return dataLoadForecast;
    };
      
    /* TODO visualize results of Load Forecast */
    const runAlgorithm = () => {
        setOpen(true);
        // const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/load_forecast/");
        props.visualizeResults(getResult());
    };

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
  
    return (
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
                {counties.map(option => (
                    <option key={option.name} value={option.residents}>
                        {option.name}
                    </option>
                ))}
            </TextField>
            <p/>
            <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
                Run
            </Button>
            <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
                <DialogTitle id="form-dialog-title">Save</DialogTitle>
                <DialogContent>
                    <DialogContentText>
        To save the results of Load Forecast for Cost Benefit Analysis, please enter your profile name.
                    </DialogContentText>
                    <TextField
                        autoFocus
                        margin="dense"
                        id="profile_name"
                        label="Profile Name"
                        fullWidth
                    />
                </DialogContent>
                <DialogActions>
                    <Button onClick={handleClose} color="primary">
        Cancel
                    </Button>
                    <Button onClick={saveResults} color="primary">
        Save
                    </Button>
                </DialogActions>
            </Dialog>
        </>
    );
}

export default AlgInputsLoadForecast;
