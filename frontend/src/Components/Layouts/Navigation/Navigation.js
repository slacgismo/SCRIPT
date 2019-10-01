import React from 'react';
import ListSubheader from '@material-ui/core/ListSubheader';
import DraftsIcon from '@material-ui/icons/Drafts';
import SendIcon from '@material-ui/icons/Send';
import Divider from '@material-ui/core/Divider';
import Paper from '@material-ui/core/Paper';
import List from '@material-ui/core/List';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import ExpandLess from '@material-ui/icons/ExpandLess';
import ExpandMore from '@material-ui/icons/ExpandMore';
import InboxIcon from '@material-ui/icons/MoveToInbox';

import NavigationNestItem from './NavigationNestItem';
import NavigationItem from './NavigationItem'

export default function navigation() {
  const [open, setOpen] = React.useState(true);

  const handleClick = () => {
      setOpen(!open);
  };

  return (
    <Paper>
    <List
      component="nav"
      aria-labelledby="nested-list-subheader"
      subheader={
        <ListSubheader component="div" id="nested-list-subheader">
          Navigation
        </ListSubheader>
      }
      >
      <NavigationItem selectedIndex={0} index={0} link={'/'} text={'Overview'} icon={<SendIcon />}/>
      <NavigationItem selectedIndex={1} index={1} link={'/Upload'} text={'Upload'} icon={<DraftsIcon />}/>
      <Divider />
      <ListItem button onClick={handleClick}>
      <ListItemIcon>
          <InboxIcon />
      </ListItemIcon>
      <ListItemText primary="Algorithms" />
      {open ? <ExpandLess /> : <ExpandMore />}
      </ListItem>
      <NavigationNestItem link={'/Algorithm1'} open={open}> Algorithm 1</NavigationNestItem>
      <NavigationNestItem link={'/Algorithm2'} open={open}> Algorithm 2</NavigationNestItem>
      <NavigationNestItem link={'/Algorithm3'} open={open}> Algorithm 3</NavigationNestItem>
      <NavigationNestItem link={'/Algorithm4'} open={open}> Algorithm 4</NavigationNestItem>


    </List>
    </Paper>
  );
}
