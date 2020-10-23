import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import TextField from "@material-ui/core/TextField";
import AlgInputsCBA from "../AlgInputs/AlgInputsCBA";
import { makeStyles } from "@material-ui/core/styles";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";

// import { dataLoadControll } from "../Api/AlgorithmData";
const useStyles = makeStyles(theme => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

function AlgorithmPageLoadControll(props) {
    const [category, setCategory] = React.useState("gas_consumption");

    const handleChange = event => {
        setCategory(event.target.value);

    };
      
    const classes = useStyles();

    return (
        <AlgorithmPage
            categoryProp = {category}
            compo= {
                <FormControl className={classes.formControl}>
                    <Select
                        labelId="label-standard-category"
                        id="standard-category"
                        onChange={handleChange}
                        value={category}
                        className={classes.selectEmpty}
                    >
                        <MenuItem value="gas_consumption">
                        Gas consumption
                        </MenuItem>
                        <MenuItem value={"load_profile"}>Load profile</MenuItem>
                        <MenuItem value={"cost_benefit"}>Cost benefit</MenuItem>
                        <MenuItem value={"net_present_value"}>Net present value</MenuItem>
                        <MenuItem value={"emission"}>Emission</MenuItem>

                    </Select>
                    <FormHelperText>Choose a category</FormHelperText>
                </FormControl>
            }
            // data={ dataLoadControll }
            title={ "Cost Benefit Analysis" }
            algInputs={ AlgInputsCBA }
        />
    );
}

export default AlgorithmPageLoadControll;
