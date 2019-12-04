// Fetch basic data
//
// axios('http://127.0.0.1:8000/api/county/')
// .then(res => {
//     const counties = res.data
//     console.log(counties)
//     this.setState({ counties })
//     console.log(this.state.counties)
// })
// .catch(console.log)

import axios from "axios";
import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import { withStyles } from "@material-ui/core/styles";
import AlgInputsLoadControl from "../AlgInputs/AlgInputsLoadControl";

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 250,
    },
  });

  /* TODO fetch couties basic data */
class CountyData extends Component {
    state = {
        counties: [],
    }

    componentDidMount() {
        axios("http://127.0.0.1:8000/api/county/")
            .then(res => {
                counties = res.data;
                console.log(counties);
                this.setState({ counties });
                console.log(this.state.counties);
            })
            .catch(console.log);
    }

    render() {
        const { classes } = this.props;
        return (
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
                    counties.map(option => (
                        <option key={option.name} value={option.residents}>
                            {option.name}
                        </option>
                    ))
                }
            </TextField>
        );
    }  
}

export default withStyles(styles, { withTheme: true})(CountyData);
