import React from "react";
import AlgorithmPage from "./AlgorithmPage";
import AlgInputsCBA from "../AlgInputs/AlgInputsCBA";
import { makeStyles } from "@material-ui/core/styles";
import Select from "@material-ui/core/Select";
import MenuItem from "@material-ui/core/MenuItem";
import FormHelperText from "@material-ui/core/FormHelperText";
import FormControl from "@material-ui/core/FormControl";

const useStyles = makeStyles((theme) => ({
    formControl: {
        margin: theme.spacing(1),
        minWidth: 120,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

function AlgorithmPageLoadControl(props) {
    const [category, setCategory] = React.useState("gas_consumption");

    const [controlType, setControlType] = React.useState("uncontrolled_values");

    const handleChange = (event) => {
        setCategory(event.target.value);
    };

    const handleControlTypeChange = (event) => {
        setControlType(event.target.value);
    };

    const classes = useStyles();

    return (
        <AlgorithmPage
            categoryProp={category}
            controlType={controlType}
            compo={
                <div>
                    <FormControl className={classes.formControl}>
                        <Select
                            labelId="label-standard-category"
                            id="standard-category"
                            onChange={handleControlTypeChange}
                            value={controlType}
                            className={classes.selectEmpty}
                        >
                            <MenuItem value={"uncontrolled_values"}>
                                Uncontrolled
                            </MenuItem>
                            <MenuItem value={"controlled_values"}>
                                Controlled
                            </MenuItem>
                        </Select>
                        <FormHelperText>
                            View uncontrolled or controlled
                        </FormHelperText>
                    </FormControl>
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
                            <MenuItem value={"load_profile"}>
                                Load profile
                            </MenuItem>
                            <MenuItem value={"cost_benefit"}>
                                Cost benefit
                            </MenuItem>
                            <MenuItem value={"net_present_value"}>
                                Net present value
                            </MenuItem>
                            <MenuItem value={"emission"}>Emission</MenuItem>
                        </Select>
                        <FormHelperText>Choose a category</FormHelperText>
                    </FormControl>
                </div>
            }
            title={"Cost Benefit Analysis"}
            algInputs={AlgInputsCBA}
        />
    );
}

export default AlgorithmPageLoadControl;
