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
import { serverUrl } from "../Api/server";
import "./AlgInputs.css";

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
            config_name: loadForecastDefaultParams.config_name,
            aggregation_level: loadForecastDefaultParams.aggregation_level,
            num_evs: loadForecastDefaultParams.num_evs,
            county_choice: loadForecastDefaultParams.county_choice,
            fast_percent: loadForecastDefaultParams.fast_percent,
            work_percent: loadForecastDefaultParams.work_percent,
            res_percent: loadForecastDefaultParams.res_percent,
            l1_percent: loadForecastDefaultParams.l1_percent,
            public_l2_percent: loadForecastDefaultParams.public_l2_percent,
            res_daily_use: loadForecastDefaultParams.res_daily_use,
            work_daily_use: loadForecastDefaultParams.work_daily_use,
            fast_daily_use: loadForecastDefaultParams.fast_daily_use,
            rent_percent: loadForecastDefaultParams.rent_percent,
            res_l2_smooth: loadForecastDefaultParams.res_l2_smooth,
            week_day: loadForecastDefaultParams.week_day,
            publicl2_daily_use: loadForecastDefaultParams.publicl2_daily_use,
            mixed_batteries: loadForecastDefaultParams.mixed_batteries,
            timer_control: loadForecastDefaultParams.timer_control,
            work_control: loadForecastDefaultParams.work_control,
            work_controls: ["PGEcev", "PGEcev_demand", "PGEcev_energy", "PGEe19", "SCEtouev8", "SDGEmedian", "SDGErandom", "cap", "minpeak"],
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

        // this.useDefaultParameters();
    }

    handleClose = () => {
        this.setState({ open: false });
    };

    update = (field, event) => {
        this.setState({ [field]: event.currentTarget.value });
    };

    getResult = async () => {
        // receives 2 lists (uncontrolled, controlled) when form is saved
        const res = await axios.get(`${ serverUrl }/algorithm/load_forecast?config=${this.state.config_name}`);
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

    saveResults = async() => {
        // check if current load forecast profile already exists before saving
        const config_res = await axios.get(`http://127.0.0.1:8000/api/config/load_forecast?config_name=${this.state.config_name}`);

        // if the CBA input relationship doesn't exist, insert new CBA input table rows to db
        if(config_res.data.length === 0){
            // change var name
            const postData = {
                config_name: this.state.config_name,
                aggregation_level: this.state.aggregation_level,
                num_evs: parseInt(this.state.num_evs),
                county: this.state.county_choice,
                fast_percent: parseFloat(this.state.fast_percent),
                work_percent: parseFloat(this.state.work_percent),
                res_percent: parseFloat(this.state.res_percent),
                l1_percent: parseFloat(this.state.l1_percent),
                public_l2_percent: parseFloat(this.state.public_l2_percent),
                res_daily_use: parseFloat(this.state.res_daily_use),
                work_daily_use: parseFloat(this.state.work_daily_use),
                fast_daily_use: parseFloat(this.state.fast_daily_use),
                rent_percent: parseFloat(this.state.rent_percent),
                res_l2_smooth: this.state.res_l2_smooth,
                week_day: this.state.week_day,
                publicl2_daily_use: parseFloat(this.state.publicl2_daily_use),
                mixed_batteries: this.state.mixed_batteries,
                timer_control: this.state.timer_control,
                work_control: this.state.work_control,
            };

            const postUrl = `${ serverUrl }/load_forecast_runner`;

            axios({
                method: "post",
                url: postUrl,
                data: postData,
            })
                .then(async (response) => {
                    console.log(response);
                    this.props.visualizeResults(await this.getResult());
                }, (error) => {
                    console.log(error);
                });
            this.setState({ open: false });
        }
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

    runAlgorithm = () => {
        this.setState({ open: true });
    };


    render() {
        const { classes } = this.props;

        const countiesTextField =
            <TextField
                id="standard-county"
                select
                className={classes.textField}
                label="Please select a county"
                SelectProps={{
                    native: true,
                    MenuProps: {
                        className: classes.menu,
                    },
                }}
                margin="normal"
                value={ this.state.county_choice }
                onChange={ e => this.update("county_choice", e) }
            >
                {
                    this.state.counties.map(option => (
                        <option key={option.name} value={option.name}>
                            {option.name}
                        </option>
                    ))
                }
            </TextField>;

        const countyNames = this.state.aggregation_level === "county" ? countiesTextField : null;

        return (
            <>
                <fieldset class="field_set">
                    <TextField
                        id="standard-aggregation_level"
                        select
                        className={classes.textField}
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        label="Please select an aggregation level"
                        margin="normal"
                        value={ this.state.aggregation_level }
                        onChange={ e => this.update("aggregation_level", e) }
                    >
                        <option key="county" value="county">
                                County
                        </option>
                        <option key="state" value="state">
                                State
                        </option>
                    </TextField>

                    { countyNames }

                    <TextField
                        id="standard-num_evs"
                        label="Total number of EVs"
                        value={ this.state.num_evs }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("num_evs", e) }
                    />
                    <TextField
                        id="standard-res_l2_smooth"
                        select
                        value={ this.state.res_l2_smooth }
                        className={classes.textField}
                        label="Residential Smooth"
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        margin="normal"
                        onChange={ e => this.update("res_l2_smooth", e) }
                    >
                        <option key="true" value="true">
                            True
                        </option>
                        <option key="false" value="false">
                            False
                        </option>
                    </TextField>
                    <TextField
                        id="standard-mixed_batteries"
                        label="Battery Mix"
                        value={ this.state.mixed_batteries }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("mixed_batteries", e) }
                    />
                </fieldset>
                <br/>
                <br/>
                {/* <br/>
                <Button variant="contained" className={classes.button} onClick={this.changeDefaultParameters}>
                    Set parameters as default
                </Button> */}
                <fieldset class="field_set">
                    <legend>Charging Types Percentage</legend>
                    <TextField
                        id="standard-fast_percent"
                        label="Fast"
                        value={ this.state.fast_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("fast_percent", e) }
                    />
                    <TextField
                        id="standard-work_percent"
                        label="Workplace"
                        value={ this.state.work_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("work_percent", e) }
                    />
                    <TextField
                        id="standard-rent_percent"
                        label="Rent"
                        value={ this.state.rent_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("rent_percent", e) }
                    />
                    <TextField
                        id="standard-res_percent"
                        label="Residential Level 2"
                        value={ this.state.res_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("res_percent", e) }
                    />
                    <TextField
                        id="standard-l1_percent"
                        label="Level 1"
                        value={ this.state.l1_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("l1_percent", e) }
                    />
                    <TextField
                        id="standard-public_l2_percent"
                        label="Public Level 2"
                        value={ this.state.public_l2_percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("public_l2_percent", e) }
                    />
                </fieldset>
                <br/>
                <br/>
                <fieldset class="field_set">
                    <legend>Charging Segment Daily Usage Percentage</legend>
                    <TextField
                        id="standard-week_day"
                        select
                        value={ this.state.week_day }
                        className={classes.textField}
                        margin="normal"
                        label="Week Day"
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        onChange={ e => this.update("week_day", e) }
                    >
                        <option key="true" value="true">
                            True
                        </option>
                        <option key="false" value="false">
                            False
                        </option>
                    </TextField>
                    <TextField
                        id="standard-res_daily_use"
                        label="Residential"
                        value={ this.state.res_daily_use }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("res_daily_use", e) }
                    />
                    <TextField
                        id="standard-work_daily_use"
                        label="Workplace"
                        value={ this.state.work_daily_use }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("work_daily_use", e) }
                    />
                    <TextField
                        id="standard-fast_daily_use"
                        label="Fast"
                        value={ this.state.fast_daily_use }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("fast_daily_use", e) }
                    />
                    <TextField
                        id="standard-publicl2_daily_use"
                        label="Public Level 2"
                        value={ this.state.publicl2_daily_use }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("publicl2_daily_use", e) }
                    />
                </fieldset>
                <br/>
                <br/>
                <fieldset class="field_set">
                    <legend>Control</legend>
                    <TextField
                        id="standard-timer_control"
                        label="Residential Timer"
                        value={ this.state.timer_control }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("timer_control", e) }
                    />
                    <TextField
                        id="standard-work_control"
                        select
                        value={ this.state.work_control }
                        className={classes.textField}
                        label="Workplace"
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        margin="normal"
                        onChange={ e => this.update("work_control", e) }
                    >
                        {
                            this.state.work_controls.map(option => (
                                <option key={option} value={option}>
                                    {option}
                                </option>
                            ))
                        }

                    </TextField>
                </fieldset>
                <br/>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.runAlgorithm}>
                    Run
                </Button>
                <Dialog open={this.state.open} onClose={this.handleClose} aria-labelledby="form-dialog-title" fullWidth={true} maxWidth={"lg"}>
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
                            value={ this.state.config_name }
                            onChange={ e => this.update("config_name", e) }
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
