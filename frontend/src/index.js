import React from 'react'
import { render } from 'react-dom'
import { BrowserRouter as Router, Route } from "react-router-dom";
import Overview from './Components/Overview/Overview';
import Upload from './Components/Upload/Upload';
import Algorithm1 from './Components/Algorithms/Algorithm1';
import Algorithm2 from './Components/Algorithms/Algorithm2';
import Algorithm3 from './Components/Algorithms/Algorithm3';
import Algorithm4 from './Components/Algorithms/Algorithm4';
import Algorithm5 from './Components/Algorithms/Algorithm5';

import About from './Components/About/About'
import * as serviceWorker from './serviceWorker';

render((
    <Router>
      <Route exact path="/" component={ Overview } />
      <Route exact path="/Upload" component={ Upload } />
      <Route exact path="/Algorithm1" component={ Algorithm1 } />
      <Route exact path="/Algorithm2" component={ Algorithm2 } />
      <Route exact path="/Algorithm3" component={ Algorithm3 } />
      <Route exact path="/Algorithm4" component={ Algorithm4 } />
      <Route exact path="/Algorithm5" component={ Algorithm5 } />
      <Route exact path="/About" component={ About } />
  
      {/* Routes for debugging single components. */}
      {/* TODO: delete these routes. */}
    </Router>
  ), document.getElementById('root'));
  serviceWorker.unregister();
