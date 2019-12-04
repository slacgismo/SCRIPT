import React from "react";
import { makeStyles } from "@material-ui/core/styles";
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
// import { profileNames } from "../Api/BasicData";
import ProfileData from "../Api/ProfileData";

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
    const [openResult, setOpenResult] = React.useState(false);
    const [openUpload, setOpenUpload] = React.useState(false);

    const handleClose = () => {
        setOpenResult(false);
        setOpenUpload(false);
    };

    /* TODO show results of Load Forecast */
    const showResults = () => {
        // TODO: backend
        // Get result of algorithm2 and visualize it
        setOpenResult(true);
    };

    // TODO: backend
    const getResult = async () => {
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
        return preprocessData(dataCBA);
    };

    const preprocessData = async (allData) => {
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

    const runAlgorithm = async () => {
        props.visualizeResults(await getResult());
    };

    const uploadFile = () => {
        setOpenUpload(true);

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

    return (
        <div>
            <ProfileData> </ProfileData>
            <Button variant="contained" className={classes.button} onClick={showResults}>
                Review
            </Button>
            <Button variant="contained" className={classes.button} onClick={uploadFile}>
                Upload
            </Button>
            <p/>
            <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
                Run
            </Button>
            
            <Dialog open={openResult} onClose={handleClose} aria-labelledby="form-dialog-title">
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

            <Dialog open={openUpload} onClose={handleClose} aria-labelledby="form-dialog-title">
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
                    <Button onClick={handleClose} color="primary">
                        Cancel
                    </Button>
                    <Button onClick={uploadFile} color="primary" >
                        Upload
                    </Button>
                </DialogActions>
            </Dialog>
        </div>
    );
}
