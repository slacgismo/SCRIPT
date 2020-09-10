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
import { ResultCharts } from "../Result/ResultCharts";
import AlgInputsLoadForecast from "../AlgInputs/AlgInputsLoadForecast";
import AlgorithmPageLoadControll from "../AlgorithmPage/AlgorithmPageCBA"

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
            loadForecastResults: [],
            processedLoadForecastResults: [],
            shouldRender: false
        };
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/config/load_forecast/")
            .then(res => {
                this.setState({ profileData: res.data });
                const profiles = res.data;
                const profileNames = [];
                for (var i = 0; i < res.data.length; i++) {
                    const profileNamesUnit = {id: "", name: ""};
                    profileNamesUnit.id = profiles[i]["id"];
                    profileNamesUnit.name = profiles[i]["config_name"];
                    profileNames.push(profileNamesUnit);
                }
                this.setState({ profileNames });
                this.setState({ profileName: document.getElementById("standard-profile").value});
            });
        
        const dataLoadForecast = [];

        axios("http://127.0.0.1:8000/api/algorithm/load_forecast").then(res => {    
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
            this.setState({ loadForecastResults: dataLoadForecast});
        });
    }

    handleClose = () => {
        this.setState({ openResult: false });
        this.setState({ openUpload: false });
    }

    showResults = async () => {
        this.setState({ openResult: true });
        this.setState({ shouldRender: true  });
        this.processLoadForecastResults(this.state.loadForecastResults);
    };

    processLoadForecastResults = async (resultArr) => {
        const data_to_visualize_all = [];
        const isTimeSeries = resultArr.length == 0 ? false : resultArr[0][Object.keys(resultArr[0])[0]][0].time ? true : false; // Time or Year
        for (const result of resultArr) {
            const data_to_visualize = {};

            for (const field of Object.keys(result)) {
                const data = result[field];
                const dataFormatted = data.map((datapoint, i) => (
                    {
                        x: isTimeSeries ? i : datapoint.year,
                        y: isTimeSeries ? parseFloat(datapoint.load) : parseFloat(datapoint.data)  // option
                    }   
                ));
                data_to_visualize[field] = {
                    yAxis: `${field}`.replace(/_/g, " "),
                    unit: "Power (kW)",
                    xAxis: isTimeSeries ? "Time" : "Year",  // TODO: other options?
                    data: dataFormatted,
                };
            }
            data_to_visualize_all.push(data_to_visualize);
        }
        this.setState({ processLoadForecastResults: data_to_visualize_all});
    };

    getResult = async () => {
        const res = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/" + this.props.category);
        const dataCBA = {dataValues: []};
        const dataCBASub = [];
        
        for (var i = 0; i < res.data.length; i++) {
            const dataCBAUnit = res.data[i];
            dataCBAUnit.values = (res.data[i].values); 
            dataCBASub.push(dataCBAUnit);
        }
        dataCBA.dataValues = dataCBASub;
        return this.preprocessData(dataCBA);
    };

    preprocessData = async (allData) => {
        const data = allData.dataValues;
        const fields = data[0] ? Object.keys(data[0].values): [0];

        // Init result
        const result = {};
        for (const field of fields) {
            result[field] = [];
        }

        data.forEach(dataItem => {
            const year = dataItem.config.year;
            const allFields = dataItem.values;
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
        return resultFlattened;
    };

    runAlgorithm = async () => {
        this.props.visualizeResults(await this.getResult());
    };

    componentDidUpdate(prevProps, prevState) {
        if (prevProps.category !== this.props.category) {
          this.runAlgorithm()
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
                        <DialogTitle onClose={this.handleClose} id="form-dialog-title">Load Forecast Profile</DialogTitle>
                        <DialogContent>    
                            <ResultCharts
                                results={ this.state.processLoadForecastResults }
                                algId={2}
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
