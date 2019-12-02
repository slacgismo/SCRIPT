import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import TextField from "@material-ui/core/TextField";
import Button from "@material-ui/core/Button";
import axios from "axios";

const useStyles = makeStyles(theme => ({
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
}));

const counties = [
    {
        name: "Santa Clara",
        residents: "1",
    },
    {
        name: "Santa Cruz",
        residents: "2",
    },
    {
        name: "San Francisco",
        residents: "3",
    },
    {
        name: "San Diego",
        residents: "4",
    },
];

export default function Scenario1 (props) {
    const runAlgorithm = async () => {
        // const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/load_controller/");
        
        // let uncontrolledLoad = JSON.parse(respResults.data[0].uncontrolled_load);
        // let controlledLoad = JSON.parse(respResults.data[0].controlled_load);

        // console.log(uncontrolledLoad);
        // console.log(controlledLoad);

        // Fake data
        const result = [
            {
                uncontrolled_load: "[{\"time\": \"0:00\", \"load\": \"6634.6\"}, {\"time\": \"1:15\", \"load\": \"6598.8\"}, {\"time\": \"2:30\", \"load\": \"6576.4\"}, {\"time\": \"3:45\", \"load\": \"6559.4\"}, {\"time\": \"0:00\", \"load\": \"6486.0\"}, {\"time\": \"1:15\", \"load\": \"6420.6\"}, {\"time\": \"2:30\", \"load\": \"6326.2\"}, {\"time\": \"3:45\", \"load\": \"6233.8\"}, {\"time\": \"0:00\", \"load\": \"6102.8\"}, {\"time\": \"1:15\", \"load\": \"5959.0\"}, {\"time\": \"2:30\", \"load\": \"5794.6\"}, {\"time\": \"3:45\", \"load\": \"5600.0\"}, {\"time\": \"0:00\", \"load\": \"5378.8\"}, {\"time\": \"1:15\", \"load\": \"5144.2\"}, {\"time\": \"2:30\", \"load\": \"4876.2\"}, {\"time\": \"3:45\", \"load\": \"4620.2\"}, {\"time\": \"0:00\", \"load\": \"4347.8\"}, {\"time\": \"1:15\", \"load\": \"4080.0\"}, {\"time\": \"2:30\", \"load\": \"3784.8\"}, {\"time\": \"3:45\", \"load\": \"3478.0\"}, {\"time\": \"0:00\", \"load\": \"3208.6\"}, {\"time\": \"1:15\", \"load\": \"2953.2\"}, {\"time\": \"2:30\", \"load\": \"2741.8\"}, {\"time\": \"3:45\", \"load\": \"2575.6\"}, {\"time\": \"0:00\", \"load\": \"2383.2\"}, {\"time\": \"1:15\", \"load\": \"2224.6\"}, {\"time\": \"2:30\", \"load\": \"2088.2\"}, {\"time\": \"3:45\", \"load\": \"1955.4\"}, {\"time\": \"0:00\", \"load\": \"1867.4\"}, {\"time\": \"1:15\", \"load\": \"1814.4\"}, {\"time\": \"2:30\", \"load\": \"1770.6\"}, {\"time\": \"3:45\", \"load\": \"1754.4\"}, {\"time\": \"0:00\", \"load\": \"1755.8\"}, {\"time\": \"1:15\", \"load\": \"1760.6\"}, {\"time\": \"2:30\", \"load\": \"1774.2\"}, {\"time\": \"3:45\", \"load\": \"1785.4\"}, {\"time\": \"0:00\", \"load\": \"1816.0\"}, {\"time\": \"1:15\", \"load\": \"1850.4\"}, {\"time\": \"2:30\", \"load\": \"1901.0\"}, {\"time\": \"3:45\", \"load\": \"1953.4\"}, {\"time\": \"0:00\", \"load\": \"1998.4\"}, {\"time\": \"1:15\", \"load\": \"2052.0\"}, {\"time\": \"2:30\", \"load\": \"2076.8\"}, {\"time\": \"3:45\", \"load\": \"2101.0\"}, {\"time\": \"0:00\", \"load\": \"2138.4\"}, {\"time\": \"1:15\", \"load\": \"2158.4\"}, {\"time\": \"2:30\", \"load\": \"2191.8\"}, {\"time\": \"3:45\", \"load\": \"2215.8\"}, {\"time\": \"0:00\", \"load\": \"2249.0\"}, {\"time\": \"1:15\", \"load\": \"2265.8\"}, {\"time\": \"2:30\", \"load\": \"2303.2\"}, {\"time\": \"3:45\", \"load\": \"2316.6\"}, {\"time\": \"0:00\", \"load\": \"2338.4\"}, {\"time\": \"1:15\", \"load\": \"2358.2\"}, {\"time\": \"2:30\", \"load\": \"2388.8\"}, {\"time\": \"3:45\", \"load\": \"2419.0\"}, {\"time\": \"0:00\", \"load\": \"2437.6\"}, {\"time\": \"1:15\", \"load\": \"2456.0\"}, {\"time\": \"2:30\", \"load\": \"2470.0\"}, {\"time\": \"3:45\", \"load\": \"2488.4\"}, {\"time\": \"0:00\", \"load\": \"2519.4\"}, {\"time\": \"1:15\", \"load\": \"2529.4\"}, {\"time\": \"2:30\", \"load\": \"2553.4\"}, {\"time\": \"3:45\", \"load\": \"2571.6\"}, {\"time\": \"0:00\", \"load\": \"2570.6\"}, {\"time\": \"1:15\", \"load\": \"2598.8\"}, {\"time\": \"2:30\", \"load\": \"2622.8\"}, {\"time\": \"3:45\", \"load\": \"2673.8\"}, {\"time\": \"0:00\", \"load\": \"2738.6\"}, {\"time\": \"1:15\", \"load\": \"2833.0\"}, {\"time\": \"2:30\", \"load\": \"3010.4\"}, {\"time\": \"3:45\", \"load\": \"3187.2\"}, {\"time\": \"0:00\", \"load\": \"3406.8\"}, {\"time\": \"1:15\", \"load\": \"3618.8\"}, {\"time\": \"2:30\", \"load\": \"3827.8\"}, {\"time\": \"3:45\", \"load\": \"4049.8\"}, {\"time\": \"0:00\", \"load\": \"4233.4\"}, {\"time\": \"1:15\", \"load\": \"4390.0\"}, {\"time\": \"2:30\", \"load\": \"4569.0\"}, {\"time\": \"3:45\", \"load\": \"4681.6\"}, {\"time\": \"0:00\", \"load\": \"4811.2\"}, {\"time\": \"1:15\", \"load\": \"4903.8\"}, {\"time\": \"2:30\", \"load\": \"5041.2\"}, {\"time\": \"3:45\", \"load\": \"5209.0\"}, {\"time\": \"0:00\", \"load\": \"5350.4\"}, {\"time\": \"1:15\", \"load\": \"5515.8\"}, {\"time\": \"2:30\", \"load\": \"5703.2\"}, {\"time\": \"3:45\", \"load\": \"5863.8\"}, {\"time\": \"0:00\", \"load\": \"6036.4\"}, {\"time\": \"1:15\", \"load\": \"6234.0\"}, {\"time\": \"2:30\", \"load\": \"6349.4\"}, {\"time\": \"3:45\", \"load\": \"6496.4\"}, {\"time\": \"0:00\", \"load\": \"6561.2\"}, {\"time\": \"1:15\", \"load\": \"6602.4\"}, {\"time\": \"2:30\", \"load\": \"6619.4\"}, {\"time\": \"3:45\", \"load\": \"6628.2\"}]",
                controlled_load: "[{\"time\": \"0:00\", \"load\": \"3531.8\"}, {\"time\": \"1:15\", \"load\": \"2741.4\"}, {\"time\": \"2:30\", \"load\": \"2175.0\"}, {\"time\": \"3:45\", \"load\": \"1735.8\"}, {\"time\": \"0:00\", \"load\": \"1398.4\"}, {\"time\": \"1:15\", \"load\": \"1139.2\"}, {\"time\": \"2:30\", \"load\": \"927.8\"}, {\"time\": \"3:45\", \"load\": \"746.6\"}, {\"time\": \"0:00\", \"load\": \"676.6\"}, {\"time\": \"1:15\", \"load\": \"597.4\"}, {\"time\": \"2:30\", \"load\": \"530.6\"}, {\"time\": \"3:45\", \"load\": \"506.6\"}, {\"time\": \"0:00\", \"load\": \"355.0\"}, {\"time\": \"1:15\", \"load\": \"305.6\"}, {\"time\": \"2:30\", \"load\": \"248.8\"}, {\"time\": \"3:45\", \"load\": \"201.6\"}, {\"time\": \"0:00\", \"load\": \"137.6\"}, {\"time\": \"1:15\", \"load\": \"144.2\"}, {\"time\": \"2:30\", \"load\": \"176.0\"}, {\"time\": \"3:45\", \"load\": \"244.2\"}, {\"time\": \"0:00\", \"load\": \"331.8\"}, {\"time\": \"1:15\", \"load\": \"391.6\"}, {\"time\": \"2:30\", \"load\": \"523.6\"}, {\"time\": \"3:45\", \"load\": \"661.2\"}, {\"time\": \"0:00\", \"load\": \"861.4\"}, {\"time\": \"1:15\", \"load\": \"1056.2\"}, {\"time\": \"2:30\", \"load\": \"1399.2\"}, {\"time\": \"3:45\", \"load\": \"1798.2\"}, {\"time\": \"0:00\", \"load\": \"2123.6\"}, {\"time\": \"1:15\", \"load\": \"2490.2\"}, {\"time\": \"2:30\", \"load\": \"2819.0\"}, {\"time\": \"3:45\", \"load\": \"3144.6\"}, {\"time\": \"0:00\", \"load\": \"3527.2\"}, {\"time\": \"1:15\", \"load\": \"3866.4\"}, {\"time\": \"2:30\", \"load\": \"4150.0\"}, {\"time\": \"3:45\", \"load\": \"4353.4\"}, {\"time\": \"0:00\", \"load\": \"4602.0\"}, {\"time\": \"1:15\", \"load\": \"4721.4\"}, {\"time\": \"2:30\", \"load\": \"4862.0\"}, {\"time\": \"3:45\", \"load\": \"4933.6\"}, {\"time\": \"0:00\", \"load\": \"4882.2\"}, {\"time\": \"1:15\", \"load\": \"4966.6\"}, {\"time\": \"2:30\", \"load\": \"4872.0\"}, {\"time\": \"3:45\", \"load\": \"4815.0\"}, {\"time\": \"0:00\", \"load\": \"4712.8\"}, {\"time\": \"1:15\", \"load\": \"4544.2\"}, {\"time\": \"2:30\", \"load\": \"4430.4\"}, {\"time\": \"3:45\", \"load\": \"4181.4\"}, {\"time\": \"0:00\", \"load\": \"3987.6\"}, {\"time\": \"1:15\", \"load\": \"3836.0\"}, {\"time\": \"2:30\", \"load\": \"3791.8\"}, {\"time\": \"3:45\", \"load\": \"3664.2\"}, {\"time\": \"0:00\", \"load\": \"3547.4\"}, {\"time\": \"1:15\", \"load\": \"3320.0\"}, {\"time\": \"2:30\", \"load\": \"3122.0\"}, {\"time\": \"3:45\", \"load\": \"2852.4\"}, {\"time\": \"0:00\", \"load\": \"2726.2\"}, {\"time\": \"1:15\", \"load\": \"2672.8\"}, {\"time\": \"2:30\", \"load\": \"2528.2\"}, {\"time\": \"3:45\", \"load\": \"2320.0\"}, {\"time\": \"0:00\", \"load\": \"2146.8\"}, {\"time\": \"1:15\", \"load\": \"2147.0\"}, {\"time\": \"2:30\", \"load\": \"2057.2\"}, {\"time\": \"3:45\", \"load\": \"2060.2\"}, {\"time\": \"0:00\", \"load\": \"2062.0\"}, {\"time\": \"1:15\", \"load\": \"2188.8\"}, {\"time\": \"2:30\", \"load\": \"2601.6\"}, {\"time\": \"3:45\", \"load\": \"3044.4\"}, {\"time\": \"0:00\", \"load\": \"3611.8\"}, {\"time\": \"1:15\", \"load\": \"4237.8\"}, {\"time\": \"2:30\", \"load\": \"4896.2\"}, {\"time\": \"3:45\", \"load\": \"5577.6\"}, {\"time\": \"0:00\", \"load\": \"6341.0\"}, {\"time\": \"1:15\", \"load\": \"7130.0\"}, {\"time\": \"2:30\", \"load\": \"7785.8\"}, {\"time\": \"3:45\", \"load\": \"8147.6\"}, {\"time\": \"0:00\", \"load\": \"8314.0\"}, {\"time\": \"1:15\", \"load\": \"8621.2\"}, {\"time\": \"2:30\", \"load\": \"8719.2\"}, {\"time\": \"3:45\", \"load\": \"8800.0\"}, {\"time\": \"0:00\", \"load\": \"8637.4\"}, {\"time\": \"1:15\", \"load\": \"8373.8\"}, {\"time\": \"2:30\", \"load\": \"8269.2\"}, {\"time\": \"3:45\", \"load\": \"8232.6\"}, {\"time\": \"0:00\", \"load\": \"7972.4\"}, {\"time\": \"1:15\", \"load\": \"8116.4\"}, {\"time\": \"2:30\", \"load\": \"8231.4\"}, {\"time\": \"3:45\", \"load\": \"8387.2\"}, {\"time\": \"0:00\", \"load\": \"8071.8\"}, {\"time\": \"1:15\", \"load\": \"7824.0\"}, {\"time\": \"2:30\", \"load\": \"7389.8\"}, {\"time\": \"3:45\", \"load\": \"6754.2\"}, {\"time\": \"0:00\", \"load\": \"5969.0\"}, {\"time\": \"1:15\", \"load\": \"5317.8\"}, {\"time\": \"2:30\", \"load\": \"4567.6\"}, {\"time\": \"3:45\", \"load\": \"3861.2\"}]",
            }
        ];
        
        const data_to_visualize = {};
        for (const field of [
            "controlled_load",
            "uncontrolled_load",
        ]) {
            const data = JSON.parse(result[0][field]);
            const dataFormatted = data.map((datapoint, i) => (
                {
                    x: i,
                    y: parseFloat(datapoint.load),
                }   
            ));
            data_to_visualize[field] = {
                yAxis: `${field}`.replace(/_/g, " "),
                unit: "kWh",
                xAxis: "Time",  // TODO: other options?
                data: dataFormatted,
            };
        }

        const data_to_visualize_all = [];
        data_to_visualize_all.push(data_to_visualize);
        props.visualizeResults(data_to_visualize_all);
    };
  
    const classes = useStyles();
  
    return (
        <div>
            <form noValidate autoComplete="off">
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
                    helperText="Please select your county"  
                    margin="normal"
                >
                    {counties.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))}
                </TextField>
                <p/>
                <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm}>
                    Run
                </Button>
            </form>    
        </div>
    );
}
