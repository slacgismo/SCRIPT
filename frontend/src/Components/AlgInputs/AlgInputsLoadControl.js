import React, {Component} from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { withStyles } from '@material-ui/core/styles';
import { countyRes } from '../Api/CountyData';
import { loadControlPromise } from '../Api/AlgorithmData';
import { loadControlDefaultParams } from '../Api/algorithmDefaultParams';
import { serverUrl } from '../Api/server';
import axios from 'axios';

const styles = theme => ({
    container: {
        display: 'flex',
        flexWrap: 'wrap',
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


class AlgInputsLoadControl extends Component {
    constructor(props) {
        super(props);
        this.state = {
            counties: ['Alameda', 'Contra Costa', 'Marin', 'Orange', 'Sacramento', 'San Francisco', 'San Mateo', 'Santa Clara', 'Solano'],
            result: null,
            county: loadControlDefaultParams.county,
            rate_structures: ['PGEcev', 'PGEcev_demand', 'PGEcev_energy', 'PGEe19', 'SCEtouev8', 'SDGEmedian', 'SDGErandom', 'cap', 'minpeak'],
            rate_structure: 'PGEe19',
        };
    }

    update = (field, event) => {
        this.setState({ [field]: event.currentTarget.value })
    };

    runAlgorithm = async () => {
        const postData = {
            county: this.state.county,
            rate_structure: this.state.rate_structure,
        }
        const postUrl = `${ serverUrl }/load_control_runner`;

        axios({
            method: 'post',
            url: postUrl,
            data: postData,
        })
        .then((response) => {
            const sca_data = [JSON.parse(response.data)]
            this.props.visualizeResults(sca_data)

        }, (error) => {
            console.log(error);
        });
    }

    render() {
        const { classes } = this.props;
        return !this.state.counties ? <></> : (
            <>
                <TextField
                    id='standart-county'
                    select
                    className={classes.textField}
                    SelectProps={{
                        native: true,
                        MenuProps: {
                            className: classes.menu,
                        },
                    }}
                    helperText='Please select a county'
                    margin='normal'
                    value={ this.state.county }
                    onChange={ e => this.update('county', e) }
                    // value={ this.state.county }
                >
                    {
                        this.state.counties.map(option => (
                            <option key={option} value={option}>
                                {option}
                            </option>
                        ))
                    }
                </TextField>

                <TextField
                    id='rate_structure'
                    select
                    value={ this.state.rate_structure }
                    className={classes.textField}
                    helperText='rate_structure'
                    SelectProps={{
                        native: true,
                        MenuProps: {
                            className: classes.menu,
                        },
                    }}
                    margin='normal'
                    onChange={ e => this.update('rate_structure', e) }
                >
                {
                    this.state.rate_structures.map(option => (
                        <option key={option} value={option}>
                            {option}
                        </option>
                    ))
                }

                </TextField>
                <br />
                <Button
                    variant='contained'
                    color='primary'
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
