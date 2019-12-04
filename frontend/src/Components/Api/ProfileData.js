import axios from "axios";
import React, {Component} from "react";
import TextField from "@material-ui/core/TextField";
import { withStyles } from "@material-ui/core/styles";

const styles = theme => ({
    textField: {
        marginLeft: theme.spacing(1),
        marginRight: theme.spacing(1),
        width: 250,
    },
});

/* Fetch profiles data */
class ProfileData extends Component {
    state = {
        profileNames:[]
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

    render() {
        const { classes } = this.props;
        return (
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
        );
    }  
}

export default withStyles(styles, { withTheme: true})(ProfileData);
