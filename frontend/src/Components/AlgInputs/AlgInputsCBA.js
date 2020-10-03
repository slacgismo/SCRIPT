import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogTitle from "@material-ui/core/DialogTitle";
import {DropzoneArea} from "material-ui-dropzone";
import axios from "axios";
import { withStyles } from "@material-ui/core/styles";
import { ResultCharts } from "../Result/ResultCharts";
import { serverUrl } from "../Api/server";
import { processResults, preprocessData } from "../Helpers/helpers";

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
            openUpload: false,
            profileNames: [],
            profileData: [],
            profileName: "",
            loadForecastResults: [],
            processedLoadForecastResults: [],
            shouldRender: false
        };
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/config/load_forecast")
            .then(res => {
                const profiles = res.data;
                const profileNames = [];
                if (profiles.length > 0) {
                    for (var i = 0; i < profiles.length; i++) {
                        const profileNamesUnit = {id: "", name: ""};
                        profileNamesUnit.id = profiles[i]["id"];
                        profileNamesUnit.name = profiles[i]["config_name"];
                        profileNames.push(profileNamesUnit);
                    }
                    this.setState({ profileData: profiles, profileNames: profileNames, profileName: document.getElementById("standard-profile").value });
                }
            });
        this.getLoadForecastData();
    }

    getLoadForecastData = async() => {
        const res = await axios.get("http://127.0.0.1:8000/api/algorithm/load_forecast", {
            params: {
                config: this.state.profileName
            }
        })
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
        this.setState({ loadForecastResults: dataLoadForecast });
    };

    handleClose = () => {
        this.setState({ openResult: false, openUpload: false });
    };

    setLoadForecastResults = () => {
        const processedLoadForecastResults = processResults(this.state.loadForecastResults);
        this.setState({ openResult: true, shouldRender: true, processedLoadForecastResults: processedLoadForecastResults  });
    };

    setProfileName = () => {
        this.setState({profileName: this.state.profileName})
    }

    findProfile = async () => {
        // check for corresponding CBA input table for current load forecast profile
        const config_res = await axios.get("http://127.0.0.1:8000/api/config/" + this.props.category, {
            params: {
                lf_config: this.state.profileName
            }
        });

        // if the CBA input relationship doesn't exist, insert new CBA input table rows to db
        if(config_res.data.length === 0){
            const postUrl = `${ serverUrl }/cost_benefit_analysis_runner`;
            const profileMatch = this.state.profileData.filter((profile) => profile.config_name === this.state.profileName);
            const countyMatch = profileMatch.map(profile => profile["choice"])
            axios({
                method: "post",
                url: postUrl,
                data: {load_profile: this.state.profileName, county: countyMatch},
            });
            this.props.visualizeResults(await this.getCBAResult());
        }
    };

    getCBAResult = async () => {
        const res = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/" + this.props.category);
        const filteredRes = res.data.filter((item) => item.config.lf_config === this.state.profileName);
        const dataCBA = {dataValues: []};
        const dataCBASub = [];          
        for (var i = 0; i < filteredRes.length; i++) {
            const dataCBAUnit = filteredRes[i];
            dataCBAUnit.values = (filteredRes[i].values); 
            dataCBASub.push(dataCBAUnit);
        }
        dataCBA.dataValues = dataCBASub;
        return preprocessData(dataCBA);
    };

    updateCharts = async () => { 
        this.props.visualizeResults(await this.getCBAResult());
    }

    updateProfileAndCharts = async () => {
        this.setState({profileName: document.getElementById("standard-profile").value});
        this.findProfile();       
        this.props.visualizeResults(await this.getCBAResult());
    };

    componentDidUpdate(prevProps, prevState) {
        // if different dropdown menu category selected (e.g. gas consumption)
        if (prevProps.category !== this.props.category) {
            this.updateCharts();
        }

        // if different load forecast profile selected, change load forecast chart
        if (prevState.profileName !== document.getElementById("standard-profile").value) {
            this.setState({profileName: document.getElementById("standard-profile").value}, () => {
                this.getLoadForecastData();
            });
        }
    }

    uploadFile = () => {
        this.setState({ openUpload: true});
        // TODO: backend
        // upload a file to EC2 as the input of algorithm 3 (cba)
    };

    render() {
        const { classes } = this.props;
        return (
            <div>
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
                    onChange={this.setProfileName}
                >
                    {
                        this.state.profileNames.map(option => (
                            <option key={option.id} value={option.name}>
                                {option.name}
                            </option>
                        ))
                    }
                </TextField>
                <Button variant="contained" className={classes.button} onClick={this.setLoadForecastResults}>
                    Review
                </Button>
                {/* <Button variant="contained" className={classes.button} onClick={this.uploadFile}>
                    Upload
                </Button> */}
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.updateProfileAndCharts}>
                    Run
                </Button>

                { !this.state.shouldRender ? <></> : (
                
                    <Dialog open={this.state.openResult} onClose={this.handleClose} aria-labelledby="form-dialog-title">
                        <DialogTitle onClose={this.handleClose} id="form-dialog-title">Load Forecast Profile</DialogTitle>
                        <DialogContent>    
                            <ResultCharts
                                results={ this.state.processedLoadForecastResults }
                                algId={ 2 }
                            />
                        </DialogContent>
                        <DialogActions>
                            <Button onClick={this.handleClose} color="primary">
                            Cancel
                            </Button>
                        </DialogActions>
                    </Dialog>
                )
                }

                <Dialog open={this.state.openUpload} onClose={this.handleClose} aria-labelledby="form-dialog-title">
                    <DialogTitle id="form-dialog-title">Upload</DialogTitle>
                    <DialogContent>
                        <DropzoneArea 
                            acceptedFiles={["text/plain"]}
                            dropzoneText = "Drag and drop a file here or click"
                            showPreviews = {true}
                            showPreviewsInDropzone = {false}
                            filesLimit = "1"
                            maxFileSize={5000000}
                            showFileNamesInPreview = "true"
                            // onChange={uploadFile} 
                        /> 
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Cancel
                        </Button>
                        <Button onClick={this.uploadFile} color="primary" >
                            Upload
                        </Button>
                    </DialogActions>
                </Dialog>
            </div>
        );
    }
}

export default withStyles(styles, { withTheme: true})(AlgInputsCBA);