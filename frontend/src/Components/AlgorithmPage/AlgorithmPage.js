import React, {Component} from "react";
import PropTypes from "prop-types";

import Base from "../../Layouts/Base";
import Content from "../../Layouts/Content";

import AlgInputs from '../AlgInputs/AlgInputs'
import ResultCharts from "../Result/ResultCharts";
import { dataLoadControll, dataLoadForecast } from "../Api/AlgorithmData";
import { makeStyles } from "@material-ui/core/styles";

import TextField from "@material-ui/core/TextField";

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

function AlgInputsLoadForecast(props) {
    const classes = useStyles();

    const algInputs = (
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
    );

    return algInputs;
}

class AlgorithmLoadControll extends Component {
    constructor(props) {
        super(props);
        this.state = {
            results: [],
        };
    }

    visualizeResults(results) {
        // Sample(Fake) result
        //
        // const resultsFake = [
        //     {
        //         yAxis: "Total Energy",
        //         xAxis: "Time",
        //         data: [
        //             {x: 1, y: 8},
        //             {x: 2, y: 10},
        //             {x: 3, y: 9},
        //             {x: 4, y: 13},
        //             {x: 5, y: 15},
        //             {x: 6, y: 10},
        //             {x: 7, y: 12},
        //             {x: 8, y: 10},
        //             {x: 9, y: 11},
        //             {x: 10, y: 12},
        //             {x: 11, y: 9},
        //             {x: 12, y: 8},
        //         ],
        //     }, {
        //         yAxis: "Total Session",
        //         xAxis: "time",
        //         data: [
        //             {x: 1, y: 8},
        //             {x: 2, y: 10},
        //             {x: 3, y: 9},
        //             {x: 4, y: 13},
        //             {x: 5, y: 15},
        //             {x: 6, y: 10},
        //             {x: 7, y: 0},
        //             {x: 8, y: 10},
        //             {x: 9, y: 11},
        //             {x: 10, y: 12},
        //             {x: 11, y: 9},
        //             {x: 12, y: 8},
        //         ],
        //     }
        // ];

        this.setState({
            results: results,
        });

        console.log(this.state.results);
    }

    render() {
        return (
            <div>
                <Base 
                    content={
                        <div>
                            <Content
                                text={`${ this.props.title } Inputs`}
                                compo={
                                    <AlgInputs
                                        title={ this.props.title }
                                        visualizeResults={ this.visualizeResults.bind(this) }
                                        data={ this.props.data }
                                        algInputs={ <AlgInputsLoadForecast /> }
                                    />
                                }
                            />
                            <br/>
                            {
                                this.state.results.length > 0 &&
                                <Content
                                    text={`${ this.props.title } Results`}
                                    compo={
                                        <ResultCharts
                                            results={ this.state.results }
                                            algId={2}
                                        />
                                    }
                                />
                            }
                        </div>
                    }/>
            </div>
        );
    }
}

export default AlgorithmLoadControll;
