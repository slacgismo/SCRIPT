import React from 'react';
import ReactDOM from 'react-dom';
import { BrowserRouter as Router, Route } from "react-router-dom";
import './index.css';
import App from './App';
import * as serviceWorker from './serviceWorker';

import OverviewMap from './components/OverviewMap'

ReactDOM.render((
  <Router>
    <Route exact path="/" component={ App } />

    {/* Routes for debugging single components. */}
    {/* TODO: delete these routes. */}
    <Route exact path="/overview-map" component={ OverviewMap } />
  </Router>
), document.getElementById('root'));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
