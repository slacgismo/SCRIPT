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

    /* TODO show results of Load Forecast*/
    const showResults = () => {
        setOpenResult(true);
    };

    /* TODO visualize results of Cost Benefit Analysis*/
    const runAlgorithm = async () => {
        // const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/cost_benefit_analysis/****");
    };

    /* TODO upload file to ec2 as inputs of algorithm3 */
    const uploadFile = () => {
        setOpenUpload(true);
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
            </form>    
        </div>
    );
}
