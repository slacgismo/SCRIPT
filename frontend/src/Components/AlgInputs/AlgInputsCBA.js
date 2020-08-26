import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import Dialog from "@material-ui/core/Dialog";
import DialogActions from "@material-ui/core/DialogActions";
import DialogContent from "@material-ui/core/DialogContent";
import DialogContentText from "@material-ui/core/DialogContentText";
import DialogTitle from "@material-ui/core/DialogTitle";
import {DropzoneArea} from "material-ui-dropzone";
import axios from "axios";
import { dataCBA } from "../Api/AlgorithmData"; // TODO: use CBA result data
import { withStyles } from "@material-ui/core/styles";
import ResultCharts from "../Result/ResultCharts";
import AlgInputsLoadForecast from "../AlgInputs/AlgInputsLoadForecast";

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

let results = [];

class AlgInputsCBA extends Component {
    constructor(props) {
        super(props);
        this.state = {
            openResult: false,
            openUpload: false,
            profileNames: [],
            profileData: [],
            profileName: "",
            county: "",
            resultsLoadForecast: [],
            shouldRender: false,
        };
    }
    
    componentDidMount() {
        axios("http://127.0.0.1:8000/api/config/load_forecast/")
            .then(res => {
                this.setState({ profileData: res.data });
                console.log("ALGINPUTS res data")
                console.log(res.data)
                const profiles = res.data;
                const profileNames = [];
                for (var i = 0; i < res.data.length; i++) {
                    const profileNamesUnit = {id: "", name: ""};
                    profileNamesUnit.id = profiles[i]["id"];
                    profileNamesUnit.name = profiles[i]["config_name"];
                    profileNames.push(profileNamesUnit);
                }
                this.setState({ profileNames });
                console.log(this.state.profileNames);
                this.setState({ profileName: document.getElementById("standard-profile").value});
                console.log(this.state.profileName);
                
            })
            .catch(console.log);
    }

    handleClose = () => {
        console.log(this);
        this.setState({ openResult: false });
        this.setState({ openUpload: false });
    }

    /* TODO show results of Load Forecast */
    showResults = async () => {
        // TODO: backend
        // Get result of algorithm2 and visualize it
        this.setState({ openResult: true });
        this.setState({ shouldRender: true  });
        
        // results = await this.getResultLoadForecast(); 
        // console.log(results);
        // // this.setState({ resultsLoadForecast: results});
        // for (var i = 0; i < this.state.profileData.length; i++) {
        //     if (this.state.profileData[i].config_name == this.state.profileName) {
        //         this.setState({ county: this.state.profileData[i].choice });
        //     }
        // }
        // console.log(this.state.resultsLoadForecast);
        // // console.log(this.state.profileName);
        // // for (var i = 0; i < this.state.profileData.length; i++) {
        // //     if (this.state.profileData[i].config_name == this.state.profileName) {
        // //         AlgInputsLoadForecast.runAlgorithm(this.state.profileData[i].choice);
                
        // //     }
        // // }
    };

    getResultLoadForecast = () => {
        this.setState({ openResult: true });
        this.setState({ shouldRender: true });
        
        // console.log(this.state.county);
        // const res = await axios.get(`http://127.0.0.1:8000/api/algorithm/load_forecast?county=${ this.state.county }`);
        const dataLoadForecast = [];
        axios.get("http://127.0.0.1:8000/api/algorithm/load_forecast").then(res => {
            console.log("RES DATA FOR LOAD FORECAST")
            console.log(res.data);
            
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
    
            for (var j = 0; j < this.state.profileData.length; j++) {
                if (this.state.profileData[j].config_name == this.state.profileName) {
                    this.setState({ county: this.state.profileData[j].choice });
                }
            }
    
            this.setState({ resultsLoadForecast: dataLoadForecast});
            
            console.log(dataLoadForecast);

        });

        return dataLoadForecast;
        // return dataLoadForecast;
    }

    // TODO: backend
    getResult = async () => {
        const res = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/gas_consumption");
        const dataCBA = {gasConsumption: []};
        const dataCBASub = [];
        console.log(res.data);
        
        for (var i = 0; i < res.data.length; i++) {
            const dataCBAUnit = res.data[i];
            console.log("DATACBAUNIT")
            console.log(dataCBAUnit)
            dataCBAUnit.consumption = (res.data[i].consumption);  
            dataCBASub.push(dataCBAUnit);
        }
        dataCBA.gasConsumption = dataCBASub;
        console.log(dataCBA);
        return this.preprocessData(dataCBA);
    };

    preprocessData = async (allData) => {
        const data = allData.gasConsumption;
        const fields = Object.keys(data[0].consumption);

        // Init result
        const result = {};
        for (const field of fields) {
            result[field] = [];
        }

        data.forEach(dataItem => {
            const year = dataItem.year;
            const allFields = dataItem.consumption;
            for (const field of fields) {
                // try {
                result[field].push({
                    year: year,
                    data: parseFloat(allFields[field]),
                });
                // } catch (error) {
                //     console.log("!!!!!!!!!!!");
                //     console.log(allFields[field]);
                // }
            }
        });

        // Flatten result
        const resultFlattened = [];
        for (const field of fields) {
            resultFlattened.push({
                [field]: result[field],
            });
        }

        console.log("preprocessed data:");
        console.log(resultFlattened);

        return resultFlattened;
    };

    runAlgorithm = async () => {
        this.props.visualizeResults(await this.getResult());
    };

    uploadFile = () => {
        this.setState({ openUpload: true});
        // TODO: backend
        // upload a file to EC2 as the input of algorithm 3 (cba)
    };

    render() {
        const { classes } = this.props;
        // this.setState({ resultsLoadForecast: this.getResultLoadForecast});
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
                >
                    {
                        this.state.profileNames.map(option => (
                            <option key={option.id} value={option.name}>
                                {option.name}
                            </option>
                        ))
                    }
                </TextField>
                <Button variant="contained" className={classes.button} onClick={this.showResults}>
                    Review
                </Button>
                {/* <Button variant="contained" className={classes.button} onClick={this.uploadFile}>
                    Upload
                </Button> */}
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.runAlgorithm}>
                    Run
                </Button>

                { !this.state.shouldRender ? <></> : (
                
                    <Dialog open={this.state.openResult} onClose={this.handleClose} aria-labelledby="form-dialog-title">
                        <DialogTitle onClose={this.handleClose} id="form-dialog-title">Results of Load Forecast</DialogTitle>
                        <DialogContent>
                            <DialogContentText> 
                        /* TODO */
                                <ResultCharts
                                    results= { this.state.resultsLoadForecast }
                                    algId={2}
                                />
                            </DialogContentText>
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
