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

class Scenario3 extends Component {
    state = {
        openResult: false,
        openUpload: false,
        profileNames: [],
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/config/load_forecast/")
            .then(res => {
                const profiles = res.data;
                const profileNames = [];
                for (var i = 0; i < res.data.length; i++) {
                    const profileNamesUnit = {id: "", name: ""};
                    profileNamesUnit.id = profiles[i]["id"];
                    profileNamesUnit.name = profiles[i]["config_name"]
                    profileNames.push(profileNamesUnit);
                }
                console.log(profileNames);
                this.setState({ profileNames });
                console.log(this.state.profileNames);                
            })
            .catch(console.log);
    }

    handleClose = () => {
        this.setState({ openResult: false })
        this.setState({ openUpload: false })
    };

    /* TODO show results of Load Forecast */
    showResults = () => {
        // TODO: backend
        // Get result of algorithm2 and visualize it
        this.setState({ openResult: true })
    };

    // TODO: backend
    getResult = async () => {
        const res = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/gas_consumption");
        const dataCBA = {gasConsumption: []};
        const dataCBASub = [];
        console.log(res.data);
        
        for (var i = 0; i < res.data.length; i++) {
            const dataCBAUnit = res.data[i];
            dataCBAUnit.consumption = JSON.parse(res.data[i].consumption);  
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
        this.setState({ openUpload: true})
        // TODO: backend
        // upload a file to EC2 as the input of algorithm 3 (cba)
    };

    // const profiles = [
    //     {
    //         name: "profile1", 
    //         id: "1"
    //     },
    //     {
    //         name: "profile2",
    //         id: "2"
    //     }
    // ];
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
                <Button variant="contained" className={classes.button} onClick={this.uploadFile}>
                    Upload
                </Button>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={this.runAlgorithm}>
                    Run
                </Button>
                
                <Dialog open={this.state.openResult} onClose={this.handleClose} aria-labelledby="form-dialog-title">
                    <DialogTitle onClose={this.handleClose} id="form-dialog-title">Results of Load Forecast</DialogTitle>
                    <DialogContent>
                        <DialogContentText> 
                        /* TODO */
                        </DialogContentText>
                    </DialogContent>
                    <DialogActions>
                        <Button onClick={this.handleClose} color="primary">
                            Cancel
                        </Button>
                    </DialogActions>
                </Dialog>

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

export default withStyles(styles, { withTheme: true})(Scenario3);
