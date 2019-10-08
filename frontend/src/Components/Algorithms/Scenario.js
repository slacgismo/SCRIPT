import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import TextField from '@material-ui/core/TextField';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid';
import Slider from '@material-ui/core/Slider';
import VolumeDown from '@material-ui/icons/VolumeDown';
import VolumeUp from '@material-ui/icons/VolumeUp';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles(theme => ({
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
}));

const currencies = [
  {
    value: 'Santa Clara',
    label: '1',
  },
  {
    value: 'Santa Cruz',
    label: '2',
  },
  {
    value: 'San Francisco',
    label: '3',
  },
  {
    value: 'San Diego',
    label: '4',
  },
];


export default function Scenario() {
  const classes = useStyles();
  const [values, setValues] = React.useState({
    name: 'Cat in the Hat',
    age: '',
    multiline: 'Controlled',
    currency: 'EUR',
  });

  const [volvalue, setValue] = React.useState(30);

  const handleChange2 = (event, newValue) => {
    setValue(newValue);
  };

  const handleChange = name => event => {
    setValues({ ...values, [name]: event.target.value });
  };

  return (
      <div>
    {/* <form  className={classes.container} noValidate autoComplete="off"> */}
    <form noValidate autoComplete="off">
      <TextField
        required
        id="standard-required"
        label="Required"
        defaultValue="2019"
        className={classes.textField}
        margin="normal"
      />
      <TextField
        id="standard-select-currency-native"
        select
        label="Select your county"
        className={classes.textField}
        value={values.currency}
        onChange={handleChange('currency')}
        SelectProps={{
          native: true,
          MenuProps: {
            className: classes.menu,
          },
        }}
        margin="normal"
      >
        {currencies.map(option => (
          <option key={option.value} value={option.value}>
            {option.value}
          </option>
        ))}
      </TextField>

      <TextField
        id="standard-helperText"
        label="Some important text"
        defaultValue="Default Value"
        className={classes.textField}
        margin="normal"
      />
      <TextField
        id="standard-with-placeholder"
        label="With placeholder"
        placeholder="Placeholder"
        className={classes.textField}
        margin="normal"
      />
   
    <div className={classes.root}>
    <br></br>
      <Typography id="continuous-slider" gutterBottom>
        Charging Control
      </Typography>
      <Grid container spacing={2}>
        <Grid item>
          <VolumeDown />
        </Grid>
        <Grid item xs>
          <Slider value={volvalue} onChange={handleChange2} aria-labelledby="continuous-slider" />
        </Grid>
        <Grid item>
          <VolumeUp />
        </Grid>
      </Grid>
    </div>
    <br></br>
    <Button variant="contained" color="primary" className={classes.button}>
        Run
    </Button>
    </form>
    
    </div>
  );
}
