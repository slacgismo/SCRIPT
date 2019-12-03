import React from "react";
import { render } from "react-dom";
import { BrowserRouter as Router, Route } from "react-router-dom";
import Overview from "./Components/Overview/Overview";
import OverviewMap from "./Components/OverviewMap/OverviewMap";
// import ResultChart from "./Components/ResultChart/ResultChart";
import Upload from "./Components/Upload/Upload";
import Download from "./Components/Download/Download";

import AlgorithmPageLoadControll from "./Components/AlgorithmPage/AlgorithmPageLoadControll";
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
        <Route exact path="/Upload" component={ Download } />
        <Route exact path="/Algorithm1" component={ AlgorithmPageLoadControll } />
        <Route exact path="/Algorithm2" component={ AlgorithmPageLoadForecast } />
        <Route exact path="/Algorithm3" component={ AlgorithmPageCBA } />
        <Route exact path="/About" component={ About } />
    </Router>
), document.getElementById("root"));

serviceWorker.unregister();
