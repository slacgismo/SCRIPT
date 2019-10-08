import React from 'react';
import PropTypes from 'prop-types';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper';
import Grid from '@material-ui/core/Grid';
import { withStyles } from '@material-ui/core/styles';

const styles = theme => ({
  paper: {
    maxWidth: 'auto',
    margin: 'auto',
    overflow: 'hidden',
  },
  block: {
    display: 'block',
  },
  addUser: {
    marginRight: theme.spacing(1),
  },
  contentWrapper: {
    margin: '20px 30px',
  },
});

function Content(props) {
  const { classes } = props;

  return (
    // <Paper>
    <Paper className={classes.paper}>
      <AppBar className={classes.searchBar} position="static" color="default" elevation={0}>
        <Toolbar>
        {/* <div className={classes.contentWrapper}> */}
        <Typography color="textSecondary" align="center">
          {props.text}
          
        </Typography>
      {/* </div> */}
      
        </Toolbar>
      </AppBar>
      <div className={classes.contentWrapper}>
        {props.compo}
      </div>
    </Paper>
    // </Paper>

  );
}

Content.propTypes = {
  classes: PropTypes.object.isRequired,
};

export default withStyles(styles)(Content);
