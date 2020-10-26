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
            advancedSettings: false,
            // Alg params
            configName: loadForecastDefaultParams.config_name,
            aggregationLevel: loadForecastDefaultParams.aggregation_level,
            numEvs: loadForecastDefaultParams.num_evs,
            countyChoice: loadForecastDefaultParams.county_choice,
            fastPercent: loadForecastDefaultParams.fast_percent,
            workPercent: loadForecastDefaultParams.work_percent,
            resPercent: loadForecastDefaultParams.res_percent,
            l1Percent: loadForecastDefaultParams.l1_percent,
            publicL2Percent: loadForecastDefaultParams.public_l2_percent,
            resDailyUse: loadForecastDefaultParams.res_daily_use,
            workDailyUse: loadForecastDefaultParams.work_daily_use,
            fastDailyUse: loadForecastDefaultParams.fast_daily_use,
            rentPercent: loadForecastDefaultParams.rent_percent,
            resL2Smooth: loadForecastDefaultParams.res_l2_smooth,
            weekDay: loadForecastDefaultParams.week_day,
            publicL2DailyUse: loadForecastDefaultParams.publicl2_daily_use,
            smallBatt: loadForecastDefaultParams.small_batt,
            bigBatt: loadForecastDefaultParams.big_batt,
            allBatt: loadForecastDefaultParams.all_batt,
            timerControl: loadForecastDefaultParams.timer_control,
            workControl: loadForecastDefaultParams.work_control,
            workControls: ["PGEcev", "PGEcev_demand", "PGEcev_energy", "PGEe19", "SCEtouev8", "SDGEmedian", "SDGErandom", "cap", "minpeak"],
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
        const res = await axios.get(`${ serverUrl }/algorithm/load_forecast?config=${this.state.configName}`);
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
        const config_res = await axios.get(`http://127.0.0.1:8000/api/config/load_forecast?config_name=${this.state.configName}`);
        // if the CBA input relationship doesn't exist, insert new CBA input table rows to db
        if(config_res.data.length === 0){
            // change var name
            const postData = {
                config_name: this.state.configName,
                aggregation_level: this.state.aggregationLevel,
                num_evs: parseInt(this.state.numEvs),
                county: this.state.countyChoice,
                fast_percent: parseFloat(this.state.fastPercent),
                work_percent: parseFloat(this.state.workPercent),
                res_percent: parseFloat(this.state.resPercent),
                l1_percent: parseFloat(this.state.l1Percent),
                public_l2_percent: parseFloat(this.state.publicL2Percent),
                res_daily_use: parseFloat(this.state.resDailyUse),
                work_daily_use: parseFloat(this.state.workDailyUse),
                fast_daily_use: parseFloat(this.state.fastDailyUse),
                rent_percent: parseFloat(this.state.rentPercent),
                res_l2_smooth: this.state.resL2Smooth,
                week_day: this.state.weekDay,
                publicl2_daily_use: parseFloat(this.state.publicL2DailyUse),
                small_batt: parseFloat(this.state.smallBatt),
                big_batt: parseFloat(this.state.bigBatt),
                all_batt: parseFloat(this.state.allBatt),
                timer_control: this.state.timerControl,
                work_control: this.state.workControl,
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

    advancedSettings = (e) => {
        e.preventDefault()
        this.setState({ advancedSettings: !this.state.advancedSettings})
    };


    render() {
        const { classes } = this.props;
        const { advancedSettings } = this.state;
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
                value={ this.state.countyChoice }
                onChange={ e => this.update("countyChoice", e) }
            >
                {
                    this.state.counties.map(option => (
                        <option key={option.name} value={option.name}>
                            {option.name}
                        </option>
                    ))
                }
            </TextField>;

        const countyNames = this.state.aggregationLevel === "county" ? countiesTextField : null;

        return (
            <>
                <fieldset class="field_set">
                    <legend>General Settings</legend>
                    <TextField
                        id="standard-aggregationLevel"
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
                        value={ this.state.aggregationLevel }
                        onChange={ e => this.update("aggregationLevel", e) }
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
                        id="standard-numEvs"
                        label="EVs in the State"
                        value={ this.state.numEvs }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("numEvs", e) }
                    />
                    <br/>
                    <br/>
                    <fieldset class="field_set">
                        <legend>Battery Capacity (must add up to 1)</legend>
                        <TextField
                            id="standard-smallBatteries"
                            label="Small"
                            value={ this.state.smallBatt }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("smallBatt", e) }
                        />
                        <TextField
                            id="standard-bigBatteries"
                            label="Big"
                            value={ this.state.bigBatt }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("bigBatt", e) }
                        />
                        <TextField
                            id="standard-allBatteries"
                            label="All"
                            value={ this.state.allBatt }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("allBatt", e) }
                        />
                    </fieldset>
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
                        id="standard-fastPercent"
                        label="Fast"
                        value={ this.state.fastPercent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("fastPercent", e) }
                    />
                    <TextField
                        id="standard-workPercent"
                        label="Workplace"
                        value={ this.state.workPercent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("workPercent", e) }
                    />
                    <TextField
                        id="standard-publicL2Percent"
                        label="Public"
                        value={ this.state.publicL2Percent }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("publicL2Percent", e) }
                    />
                    <br/>
                    <br/>
                    <fieldset class="field_set">
                        <legend>Residential (must add up to 1)</legend>
                        <TextField
                            id="standard-l1Percent"
                            label="Level 1"
                            value={ this.state.l1Percent }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("l1Percent", e) }
                        />
                        <TextField
                            id="standard-resPercent"
                            label="Level 2"
                            value={ this.state.resPercent }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("resPercent", e) }
                        />
                        <TextField
                            id="standard-rentPercent"
                            label="MUD"
                            value={ this.state.rentPercent }
                            className={classes.textField}
                            margin="normal"
                            onChange={ e => this.update("rentPercent", e) }
                        />
                    </fieldset>
                </fieldset>
                <br/>
                <br/>
                <fieldset class="field_set">
                    <legend>Control</legend>
                    <TextField
                        id="standard-timerControl"
                        label="Residential Timer"
                        value={ this.state.timerControl }
                        className={classes.textField}
                        margin="normal"
                        onChange={ e => this.update("timerControl", e) }
                    />
                    <TextField
                        id="standard-workControl"
                        select
                        value={ this.state.workControl }
                        className={classes.textField}
                        label="Workplace"
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        margin="normal"
                        onChange={ e => this.update("workControl", e) }
                    >
                        {
                            this.state.workControls.map(option => (
                                <option key={option} value={option}>
                                    {option}
                                </option>
                            ))
                        }

                    </TextField>
                    <TextField
                        id="standard-resL2Smooth"
                        select
                        value={ this.state.resL2Smooth }
                        className={classes.textField}
                        label="Residential Smooth"
                        SelectProps={{
                            native: true,
                            MenuProps: {
                                className: classes.menu,
                            },
                        }}
                        margin="normal"
                        onChange={ e => this.update("resL2Smooth", e) }
                    >
                        <option key="true" value="true">
                            True
                        </option>
                        <option key="false" value="false">
                            False
                        </option>
                    </TextField>
                </fieldset>
                <br/>
                <br/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.advancedSettings}>Advanced Settings</Button>
                {   advancedSettings
                    ?
                        <fieldset class="field_set">
                            <legend>Advanced Settings</legend>
                            <TextField
                                id="standard-weekDay"
                                select
                                value={ this.state.weekDay }
                                className={classes.textField}
                                margin="normal"
                                label="Day Type"
                                SelectProps={{
                                    native: true,
                                    MenuProps: {
                                        className: classes.menu,
                                    },
                                }}
                                onChange={ e => this.update("weekDay", e) }
                            >
                                <option key="true" value="true">
                                    Week Day
                                </option>
                                <option key="false" value="false">
                                    Week End
                                </option>
                            </TextField>
                            <TextField
                                id="standard-resDailyUse"
                                label="Residential"
                                value={ this.state.resDailyUse }
                                className={classes.textField}
                                margin="normal"
                                onChange={ e => this.update("resDailyUse", e) }
                            />
                            <TextField
                                id="standard-workDailyUse"
                                label="Workplace"
                                value={ this.state.workDailyUse }
                                className={classes.textField}
                                margin="normal"
                                onChange={ e => this.update("workDailyUse", e) }
                            />
                            <TextField
                                id="standard-fastDailyUse"
                                label="Fast"
                                value={ this.state.fastDailyUse }
                                className={classes.textField}
                                margin="normal"
                                onChange={ e => this.update("fastDailyUse", e) }
                            />
                            <TextField
                                id="standard-publicL2DailyUse"
                                label="Public Level 2"
                                value={ this.state.publicL2DailyUse }
                                className={classes.textField}
                                margin="normal"
                                onChange={ e => this.update("publicL2DailyUse", e) }
                            />
                        </fieldset>
                    : null
                }
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
                            value={ this.state.configName }
                            onChange={ e => this.update("configName", e) }
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
