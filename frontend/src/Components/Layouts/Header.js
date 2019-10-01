import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import MenuIcon from '@material-ui/icons/Menu';
import Avatar from '@material-ui/core/Avatar';

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
    //height: 100
  },

  title: {
    textAlign: 'center',
    flexGrow: 1,
    // height: 100
  },
}));

export default function ButtonAppBar() {
  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar  position="static">
        <Toolbar>
          <Avatar edge="start" color="inherit" aria-label="menu">
            <MenuIcon />
          </Avatar>
          <Typography variant="h6" className={classes.title}>
            Smart Charging Infrastructure Planning Tool (SCRIPT)
          </Typography>
          
        </Toolbar>
      </AppBar>
      
    </div>
  );
}
