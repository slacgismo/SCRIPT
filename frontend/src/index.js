import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Overview from "./Components/Overview/Overview";
import OverviewMap from "./Components/OverviewMap/OverviewMap";
// import ResultChart from "./Components/ResultChart/ResultChart";
import Upload from "./Components/Upload/Upload";
import Download from "./Components/Download/Download";
import AlgorithmLoadControll from "./Components/Algorithms/AlgorithmLoadControll";
import Algorithm2 from "./Components/Algorithms/Algorithm2";
import Algorithm3 from "./Components/Algorithms/Algorithm3";
import About from "./Components/About/About";
import * as serviceWorker from "./serviceWorker";

render((
    <Router>
        <Route exact path="/" component={ Overview } />
        <Route exact path="/Upload" component={ Download } />
        <Route exact path="/Algorithm1" component={ AlgorithmLoadControll } />
        <Route exact path="/Algorithm2" component={ Algorithm2 } />
        <Route exact path="/Algorithm3" component={ Algorithm3 } />
        <Route exact path="/About" component={ About } />
  
        {/* Routes for debugging single components. */}
        {/* TODO: delete these routes. */}
        {/* <Route exact path="/overview-map" component={ OverviewMap } />
        <Route exact path="/result-chart" component={ ResultChart } /> */}
    </Router>
), document.getElementById("root"));

serviceWorker.unregister();
