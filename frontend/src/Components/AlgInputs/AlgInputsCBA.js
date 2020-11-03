import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import DialogContentText from "@material-ui/core/DialogContentText";
import { withStyles } from "@material-ui/core/styles";
import axios from "axios";
import { ResultCharts } from "../Result/ResultCharts";
import { serverUrl } from "../Api/server";
import { processResults, preprocessData, checkFlowerTaskStatus, exponentialBackoff } from "../Helpers/helpers";

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

class AlgInputsCBA extends Component {
    constructor(props) {
        super(props);
        this.state = {
            openResult: false,
            shouldRender: false,
            openAlert: false,
            alertTitle: "",
            alertDescription: "",
            profileName: "",
            profileNames: [],
            profileData: [],
            loadForecastResults: [],
            chartTitles: []  
        };
    }

    componentDidMount() {
        axios({
            url: `${ serverUrl }/config/load_forecast`,
            method: "get"
        })
            .then(res => {
                const profiles = res.data;
                const profileNames = [];
                if (profiles.length > 0) {
                    for (var i = 0; i < profiles.length; i++) {
                        const profileNamesUnit = {name: ""};
                        profileNamesUnit.name = profiles[i]["config_name"];
                        profileNames.push(profileNamesUnit);
                    }
                    this.setState({ profileData: profiles, profileNames: profileNames, profileName: profileNames[0].name });
                }
            }, (error) => {
                this.handleAlertOpen("", "Server Error");
            });
    }

    getLoadForecastData = () => {
        axios({
            url: `${ serverUrl }/algorithm/load_forecast`,
            method: "get",
            params: {
                config: this.state.profileName
            }
        })
            .then(async (lf_res) => {
                const dataLoadForecast = [];
                for (var i = 0; i < lf_res.data.length; i++) {
                    const dataLoadForecastUnit = {residential_l1_load: "", residential_l2_load: "", residential_mud_load: "", work_load: "", fast_load: "", public_l2_load: "", total_load: ""};
                    dataLoadForecastUnit.residential_l1_load = (lf_res.data[i].residential_l1_load);
                    dataLoadForecastUnit.residential_l2_load = (lf_res.data[i].residential_l2_load);
                    dataLoadForecastUnit.residential_mud_load = (lf_res.data[i].residential_mud_load);
                    dataLoadForecastUnit.work_load = (lf_res.data[i].work_load);
                    dataLoadForecastUnit.fast_load = (lf_res.data[i].fast_load);
                    dataLoadForecastUnit.public_l2_load = (lf_res.data[i].public_l2_load);
                    dataLoadForecastUnit.total_load = (lf_res.data[i].total_load);
                    dataLoadForecast.push(dataLoadForecastUnit);
                    this.setLoadForecastResults(dataLoadForecast);
                }
            }, (error) => {
                this.handleAlertOpen("Error", "Error occured while loading load forecast profile.");
            });
    };

    setLoadForecastResults = (loadForecastData) => {
        const loadForecastResults = processResults(loadForecastData);
        const profileMatch = this.state.profileData.filter((profile) => profile.config_name === this.state.profileName)[0];
        const countyChoice = profileMatch["choice"];
        const rateStructure = profileMatch["work_control"];
        this.setState({ chartTitles: [`${this.state.profileName} - ${countyChoice} uncontrolled`, `${this.state.profileName} - ${countyChoice} ${rateStructure} controlled`] });
        this.setState({ openResult: true, shouldRender: true, loadForecastResults: loadForecastResults  });
    };

    findProfile = () => {
        axios({
            url: `${ serverUrl }/config/${ this.props.category }/`,
            method: "get",
            params: {
                lf_config: this.state.profileName
            }
        })
            .then(async (configRes) => {
                if(!configRes.data.length){
                    this.props.loadingResults(true);
                    const profileMatch = this.state.profileData.filter((profile) => profile.config_name === this.state.profileName);
                    const countyMatch = profileMatch.map(profile => profile["choice"]);
                    axios({
                        url: `${ serverUrl }/cost_benefit_analysis_runner`,
                        method: "post",
                        data: {load_profile: this.state.profileName, county: countyMatch}

                    })
                        .then(async (cbaRes) =>  {
                            const taskId = cbaRes.data.task_id;
                            let timeout;
                            await exponentialBackoff(checkFlowerTaskStatus, taskId, timeout, 20, 75, 
                                async () => { 
                                    this.props.loadingResults(false); 
                                    this.props.visualizeResults(await this.getCBAResult());
                                }, 
                                () => {
                                    this.props.loadingResults(false); 
                                    this.handleAlertOpen("Error", "Error occured while running cost benefit analysis.");
                                }
                            );
                        }, (error) => {
                            this.props.loadingResults(false); 
                            this.handleAlertOpen("Error", "Error occured while attempting to start the cost benefit analysis runner.");
                        });
                }
            }, (error) => {
                this.handleAlertOpen("", "Server error");
            });
    }

    getCBAResult = async () => {
        axios({
            url: `${ serverUrl }/algorithm/cost_benefit_analysis/${ this.props.category }`,
            method: "get"
        })
            .then(async (res) => {
                const filteredRes = res.data.filter((item) => item.config.lf_config === this.state.profileName);
                const dataCBA = {dataValues: []};
                const dataCBASub = [];
                for (var i = 0; i < filteredRes.length; i++) {
                    const dataCBAUnit = filteredRes[i];
                    dataCBAUnit.values = (filteredRes[i][this.props.controlType]); 
                    dataCBASub.push(dataCBAUnit);
                }
                dataCBA.dataValues = dataCBASub;
                return preprocessData(dataCBA);
            }, (error) => {
                this.handleAlertOpen("", "Server error");
            });
    };

    handleAlertOpen = (title, description) => {
        this.setState({ alertTitle: title, alertDescription: description, openAlert: true});
    };

    handleAlertClose = () => {
        this.setState({ openAlert: false});
    };

    handleChartsClose = () => {
        this.setState({ openResult: false, openUpload: false });
    };

    updateCharts = async () => {
        this.props.visualizeResults(await this.getCBAResult());
    };

    updateProfileAndCharts = async () => {
        this.findProfile();
        this.props.visualizeResults(await this.getCBAResult());
    };

    loadedResultsandCharts = async () => {
        this.props.loadingResults(false);
        this.props.visualizeResults(await this.getCBAResult());
    };

    update = (field, event) => {
        this.setState({ [field]: event.currentTarget.value });
    };

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.category !== this.props.category) {
            this.updateCharts();
        }
        if (prevProps.controlType !== this.props.controlType) {
            this.updateCharts();
        }
        if (prevState.profileName !== this.state.profileName) {
            this.getLoadForecastData();
        }
    }

    render() {
        const { classes } = this.props;
        return (
            <div>
                <Dialog
                    open={this.state.openAlert}
                    onClose={this.handleAlertClose}
                    aria-labelledby="alert-dialog-title"
                    aria-describedby="alert-dialog-description"
                >
                    <DialogTitle id="alert-dialog-title">{this.state.alertTitle}</DialogTitle>
                    <DialogContent>
                        <DialogContentText id="alert-dialog-description">
                            {this.state.alertDescription}
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleAlertClose} color="primary" autoFocus>
                            OK
                        </Button>
                    </DialogActions>
                </Dialog>
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
                    onChange={ e => this.update("profileName", e)}
                >
                    {
                        this.state.profileNames.map(option => (
                            <option key={option.name} value={option.name}>
                                {option.name}
                            </option>
                        ))
                    }
                </TextField>
                <Button variant="contained" className={classes.button} onClick={this.getLoadForecastData}>
                    Review
                </Button>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.updateProfileAndCharts}>
                    Run
                </Button>

                { !this.state.shouldRender ? <></> : (

                    <Dialog open={this.state.openResult} onClose={this.handleChartsClose} aria-labelledby="form-dialog-title">
                        <DialogTitle onClose={this.handleChartsClose} id="form-dialog-title">Load Forecast Profile</DialogTitle>
                        <DialogContent>
                            <ResultCharts
                                results={ this.state.loadForecastResults }
                                algId={ 2 }
                                chartTitles={ this.state.chartTitles }
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={this.handleChartsClose} color="primary">
                            Cancel
                            </Button>
                        </DialogActions>
                    </Dialog>
                )
                }
            </div>
        );
    }
}

export default withStyles(styles, { withTheme: true})(AlgInputsCBA);
