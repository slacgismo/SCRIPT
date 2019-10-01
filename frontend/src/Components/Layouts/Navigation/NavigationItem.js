import React from 'react';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import {Link} from 'react-router-dom'

export default function navigationItem(props) {
    const [selectedIndex, setSelectedIndex] = React.useState(0);

    const handleListItemClick = (event, index) => {
        console.log(index);
        setSelectedIndex(index);
      };

    const index = props.index;
    // console.log(index);
    const selected = props.selected;

    return (
    <ListItem 
      component={Link}
      to={props.link}
      selected={selectedIndex === selected}
      onClick={event => handleListItemClick(event, index)}
      button>
        <ListItemIcon>
          {props.icon}
        </ListItemIcon>
        <ListItemText primary={props.text} />
    </ListItem>
    )
}