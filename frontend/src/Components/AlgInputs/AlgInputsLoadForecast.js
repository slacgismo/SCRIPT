import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import { withStyles } from "@material-ui/core/styles";
import axios from "axios";
import { loadForecastPromise, fieldsLoadForecast } from "../Api/AlgorithmData";
import { countyRes } from "../Api/CountyData";
import { loadForecastDefaultParams } from "../Api/algorithmDefaultParams";

const styles = theme => ({
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
});



class AlgInputsLoadForecast extends Component {
    constructor(props) {
        super(props);
        this.state = {
            open: false,
            counties: [],

            // Alg params
            aggregation_level: "",
            num_evs: null,
            county_choice: "",
            fast_percent: 0.1,
            work_percent: 0.2,
            res_percent: 0.7,
            l1_percent: 0.5,
            publicl2_percent: 0.0,

            res_daily_use: 1.0,
            work_daily_use: 1.0,
            fast_daily_use: 0.5,
            rent_percent: 0.4,
        };
    }

    componentDidMount() {
        countyRes.then(res => {
            this.setState({
                counties: res.data,
            });
        });

        loadForecastPromise.then(res => {
            const result = [];
            res.data.forEach(data => {
                const filteredData = {};
                fieldsLoadForecast.forEach(field => {
                    filteredData[field] = data[field];
                });
                result.push(filteredData);
            });
            this.setState({
                result: result,
            });
        });

        this.useDefaultParameters();
    }

    handleClose = () => {
        this.setState({ open: false});
    };

    /* TODO save results(profile) of Load Forecast*/
    saveResults = () => {
        this.setState({ open: false});
        // TODO: backend
        // POST data to save as a profile
    };

    // TODO: backend
    getResult = async (county) => {
        this.setState({ county: document.getElementById("standard-county").value });
        console.log(county);
        const res = await axios.get(`http://127.0.0.1:8000/api/algorithm/load_forecast?county=${ county }`);
        console.log(res.data);
        const dataLoadForecast = [];
        for (var i = 0; i < res.data.length; i++) {
            const  dataLoadForecastUnit = {residential_l1_load: "", residential_l2_load: "", residential_mud_load: "", work_load: "", fast_load: "", public_l2_load: "", total_load: ""};
            dataLoadForecastUnit.residential_l1_load = (res.data[i].residential_l1_load);
            dataLoadForecastUnit.residential_l2_load = (res.data[i].residential_l2_load);
            dataLoadForecastUnit.residential_mud_load = (res.data[i].residential_mud_load);
            dataLoadForecastUnit.work_load = (res.data[i].work_load);
            dataLoadForecastUnit.fast_load = (res.data[i].fast_load);
            dataLoadForecastUnit.public_l2_load = (res.data[i].public_l2_load);
            dataLoadForecastUnit.total_load = (res.data[i].total_load);
            dataLoadForecast.push(dataLoadForecastUnit);
        }

        return dataLoadForecast;
    };

    useDefaultParameters = () => {
        // TODO: backend * 3
        // Get default parameter set

        Object.keys(loadForecastDefaultParams).forEach(param => {
            this.setState({
                [param]: loadForecastDefaultParams[param],
            });
        });
    }
      
    runAlgorithm = async (county) => {
        this.setState({ open: true });
        this.props.visualizeResults(await this.getResult(county));
    };
  
    render() {
        const { classes } = this.props;
        return (
            <>
                <TextField
                    id="standard-county"
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
                        this.state.counties.map(option => (
                            <option key={option.name} value={option.name}>
                                {option.name}
                            </option>
                        ))
                    }
                </TextField>
                {/* <br/>
                <Button variant="contained" className={classes.button} onClick={this.changeDefaultParameters}>
                    Set parameters as default
                </Button> */}
                <br/>
                <TextField
                    id="standard-aggregation_level"
                    label="aggregation_level"
                    value={ this.state.aggregation_level }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-num_evs"
                    label="num_evs"
                    value={ this.state.num_evs }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-fast_percent"
                    label="fast_percent"
                    value={ this.state.fast_percent }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-work_percent"
                    label="work_percent"
                    value={ this.state.work_percent }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-res_percent"
                    label="rate_res_percent"
                    value={ this.state.res_percent }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-l1_percent"
                    label="l1_percent"
                    value={ this.state.l1_percent }
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    id="standard-public_l2_percent"
                    label="public_l2_percent"
                    value={ this.state.publicl2_percent }
                    className={classes.textField}
                    margin="normal"
                />
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.runAlgorithm}>
                    Run
                </Button>
                <Dialog open={this.state.open} onClose={this.handleClose} aria-labelledby="form-dialog-title">
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
                        <Button onClick={this.handleClose} color="primary">
                            Cancel
                        </Button>
                        <Button onClick={this.saveResults} color="primary">
                            Save
                        </Button>
                    </DialogActions>
                </Dialog>
            </>
        );
    }
}
export default withStyles(styles, { withTheme: true})(AlgInputsLoadForecast);
