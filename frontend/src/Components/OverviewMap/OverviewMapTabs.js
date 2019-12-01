import React from "react";
import PropTypes from "prop-types";
import SwipeableViews from "react-swipeable-views";
import { makeStyles, useTheme } from "@material-ui/core/styles";
import AppBar from "@material-ui/core/AppBar";
import Tabs from "@material-ui/core/Tabs";
import Tab from "@material-ui/core/Tab";
import Typography from "@material-ui/core/Typography";
import Box from "@material-ui/core/Box";
import Button from "@material-ui/core/Button";
import OverviewMap from "./OverviewMap";

const useStyles = makeStyles(theme => ({
    button: {
        margin: theme.spacing(1),
    },
    input: {
        display: "none",
    },
}));

function OverviewMapTabs(props) {
    const classes = useStyles();
    
    return (
        <>
            <Button
                className={classes.button}
                onClick={ props.updateMap("totalEnergy") }
            >
          Total Energy
            </Button>
            {/* <Button */}
            {/*   className={classes.button} */}
            {/*   onClick={ props.updateMap("totalSession") } */}
            {/* > */}
            {/*   Total Session */}
            {/* </Button> */}
        </>
    );
}

export default OverviewMapTabs;
