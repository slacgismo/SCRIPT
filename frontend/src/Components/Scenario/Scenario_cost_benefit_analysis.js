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

export default function Scenario3 (props) {
    const classes = useStyles();
    const [open, setOpen] = React.useState(false);

    const handleClose = () => {
        setOpen(false);
    };

    /* TODO show results of Load Forecast*/
    const showResults = () => {
        setOpen(true);
    };

    /* TODO visualize results of Cost Benefit Analysis*/
    const runAlgorithm = async () => {
        // const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/****");
    };

    return (
        <div>
            <form noValidate autoComplete="off">
                <TextField
                    id="standard-profile"
                    select
                    className={classes.textField}
                    SelectProps={{
                        native: true,
                        MenuProps: {
                            className: classes.menu,
                        },
                    }}
                    helperText="Please select a profile"
                    margin="normal"
                >
                    {props.profiles.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))}
                </TextField>
                <Button variant="contained" className={classes.button} onClick={showResults}>
                    Review
                </Button>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
                    Run
                </Button>
                <Dialog open={open} onClose={handleClose} aria-labelledby="form-dialog-title">
                    <DialogTitle onClose={handleClose} id="form-dialog-title">Results of Load Forecast</DialogTitle>
                    <DialogContent>
                        <DialogContentText>
                        /* TODO */
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={handleClose} color="primary">
                            Cancel
                        </Button>
                    </DialogActions>
                </Dialog>
            </form>    
        </div>
    );
}
