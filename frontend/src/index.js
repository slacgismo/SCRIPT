import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Overview from "./Components/Overview/Overview";
import OverviewMap from "./Components/OverviewMap/OverviewMap";
import ResultChart from "./Components/ResultChart/ResultChart";
import Upload from "./Components/Upload/Upload";
import Download from "./Components/Download/Download";
import Load_controll from "./Components/Algorithms/Load_controll";
import Load_forecast from "./Components/Algorithms/Load_forecast";
import Cost_benefit_analysis from "./Components/Algorithms/Cost_benefit_analysis";
import About from "./Components/About/About";
import * as serviceWorker from "./serviceWorker";

render((
    <Router>
        <Route exact path="/" component={ Overview } />
        <Route exact path="/Upload" component={ Download } />
        <Route exact path="/Load Controll" component={ Load_controll } />
        <Route exact path="/Load Forecast" component={ Load_forecast } />
        <Route exact path="/Cost Benefit Analysis" component={ Cost_benefit_analysis } />
        <Route exact path="/About" component={ About } />
  
        {/* Routes for debugging single components. */}
        {/* TODO: delete these routes. */}
        <Route exact path="/overview-map" component={ OverviewMap } />
        <Route exact path="/result-chart" component={ ResultChart } />
    </Router>
), document.getElementById("root"));

serviceWorker.unregister();
