import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Overview from "./Components/Overview/Overview";
import OverviewMap from "./Components/OverviewMap/OverviewMap";
import OverviewMapLegend from "./Components/OverviewMap/OverviewMapLegend";
// import ResultChart from "./Components/ResultChart/ResultChart";
import Upload from "./Components/Upload/Upload";
import Download from "./Components/Download/Download";

import AlgorithmPageLoadControl from "./Components/AlgorithmPage/AlgorithmPageLoadControl";
import AlgorithmPageLoadForecast from "./Components/AlgorithmPage/AlgorithmPageLoadForecast";
import AlgorithmPageCBA from "./Components/AlgorithmPage/AlgorithmPageCBA";

// import Load_controll from "./Components/Algorithms/Load_controll";
// import Load_forecast from "./Components/Algorithms/Load_forecast";
// import Cost_benefit_analysis from "./Components/Algorithms/Cost_benefit_analysis";

import About from "./Components/About/About";
import * as serviceWorker from "./serviceWorker";

render((
    <Router>
        <Route exact path="/" component={ Overview } />
        <Route exact path="/upload" component={ Download } />
        <Route exact path="/alg-loadcontrol" component={ AlgorithmPageLoadControl } />
        <Route exact path="/alg-loadforecast" component={ AlgorithmPageLoadForecast } />
        <Route exact path="/alg-cba" component={ AlgorithmPageCBA } />
        <Route exact path="/about" component={ About } />
        
        {/* TODO: delete. Only for debug-purpose */}
        <Route exact path="/legend" component={ OverviewMapLegend } />
    </Router>
), document.getElementById("root"));

serviceWorker.unregister();
