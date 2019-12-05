import React, {Component} from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import { withStyles } from "@material-ui/core/styles";
import { dataLoadControll } from "../Api/AlgorithmData";
import { countyRes } from "../Api/CountyData";
import axios from "axios";

const styles = theme => ({
    container: {
        display: "flex",
        flexWrap: "wrap",
    },
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 200,
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

// const counties = [
//     {
//         name: "Santa Clara",
//         residents: "1",
//     },
//     {
//         name: "Santa Cruz",
//         residents: "2",
//     },
//     {
//         name: "San Francisco",
//         residents: "3",
//     },
//     {
//         name: "San Diego",
//         residents: "4",
//     },
// ];



class AlgInputsLoadControl extends Component {
    constructor(props) {
        super(props);
        this.state = {
            counties: [],
        };
    }

    componentDidMount() {
        countyRes.then(res => {
            console.log("888888");
            console.log(res.data);
            this.setState({
                counties: res.data,
            });   
        });
    }

    /* TODO change default parameters of Load Controll */
    changeDefaultParameters() {
        // TODO: backend * 3
        // Get default parameter set
    }

    // TODO: backend
    async getResult() {
        var county = document.getElementById("standart-county").value;
        console.log(county);
        const res = await axios.get(`http://127.0.0.1:8000/api/algorithm/load_controller/?county=${ county }`);
        // console.log(res.data);
        const dataLoadControll = [];
        for (var i = 0; i < res.data.length; i++) {
            const  dataLoadControllUnit = {uncontrolled_load: "", controlled_load: ""};
            dataLoadControllUnit.uncontrolled_load = JSON.parse(res.data[i].uncontrolled_load);
            dataLoadControllUnit.controlled_load = JSON.parse(res.data[i].controlled_load);
            dataLoadControll.push(dataLoadControllUnit);
        }
        console.log(dataLoadControll);
        return dataLoadControll;
    }

    async runAlgorithm() {
        this.props.visualizeResults(await this.getResult());
    }


    render() {
        const { classes } = this.props;
        return !this.state.counties ? <></> : (
            <>
                <TextField
                    id="standart-county"
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
                            <option key={option.name} value={option.residents}>
                                {option.name}
                            </option>
                        ))
                    }
                </TextField>
                <br />
                <Button variant="contained" className={classes.button} onClick={this.changeDefaultParameters}>
                    Default parameters
                </Button>
                <br/>
                <TextField
                    disabled
                    id="standard-rate_energy_peak"
                    label="rate_energy_peak"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    disabled
                    id="standard-rate_energy_partpeak"
                    label="rate_energy_partpeak"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    disabled
                    id="standard-rate_energy_offpeak"
                    label="rate_energy_offpeak"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    disabled
                    id="standard-rate_demand_peak"
                    label="rate_demand_peak"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    disabled
                    id="standard-rate_demand_partpeak"
                    label="rate_demand_partpeak"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <TextField
                    disabled
                    id="standard-rate_demand_overall"
                    label="rate_demand_overall"
                    defaultValue="defaulValue"
                    className={classes.textField}
                    margin="normal"
                />
                <br />
                <Button
                    variant="contained"
                    color="primary"
                    className={classes.button}
                    onClick={ () => this.runAlgorithm() }
                >
                Run
                </Button>
            </>
        );
    }
    
}

export default withStyles(styles, { withTheme: true})(AlgInputsLoadControl);
