import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardContent from '@material-ui/core/CardContent';
import Typography from '@material-ui/core/Typography';

const useStyles = makeStyles({
  card: {
    minWidth: 275,
    backgroundColor: '#D3D3D3'
  },
  title: {
    fontSize: 14,
  },
});

export default function SimpleCard() {
  const classes = useStyles();

  return (
    <Card className={classes.card}>
      <CardContent>
        <Typography className={classes.title} color="textSecondary" gutterBottom>
        <p>address: 
         <br/>phone:
         <br/>email:
         <br/>mailbox:</p>
        </Typography>
      </CardContent>
    </Card>
  );
}
