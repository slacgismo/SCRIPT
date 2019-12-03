import React from "react";
import "../../../node_modules/react-vis/dist/style.css";
import {
    XYPlot,
    LineSeries,
    HorizontalGridLines,
    XAxis,
    YAxis,
    // Borders,
    ChartLabel,
    DiscreteColorLegend
} from "react-vis";
import "./ResultChart.css";
import { relative } from "path";

class ResultChart extends React.Component {
    constructor(props) {
        super(props);
    }

    render() {
        const colors = [
            "#e62020",
            "#e3b920",
            "#63b81a",
            "#25c3db",
            "#3b22e0",
            "#c921db",
            "#911955",
            
            "#e62020",
            "#e3b920",
            "#63b81a",
            "#25c3db",
            "#3b22e0",
            "#c921db",
            "#911955",

            "#e62020",
            "#e3b920",
            "#63b81a",
            "#25c3db",
            "#3b22e0",
            "#c921db",
            "#911955",
        ];
        const { results } = this.props;

        console.log("Results in a chart");
        console.log(results);

        const newItems = [];
        const newData = [];
        Object.keys(results).forEach((attr, i) => {
            newItems.push({
                title: results[attr].yAxis,
                color: colors[i],
            });
            newData.push({
                key: attr,
                data: results[attr].data,
                color: colors[i],
            });
        });

        return (
            <div className="chart-grid">
                <XYPlot height={600} width={800}>
                    <DiscreteColorLegend
                        style={{
                            position: "absolute",
                            left: "850px",
                            top: "15px",
                            width: "30rem",
                        }}
                        orientation="vertical"
                        items={ newItems }
                    />
                        
                    <HorizontalGridLines />
                        
                    {
                        newData.map(newDataPiece => (
                            <LineSeries
                                key={ newDataPiece.key }
                                data={ newDataPiece.data }
                                color={ newDataPiece.color }
                            />
                        ))
                    }
                        
                    <XAxis
                        // title={ this.props.results[Object.keys(this.props.results)[0]].xAxis }
                        position="end"
                        tickFormat={(d) => {
                            if (this.props.results[Object.keys(this.props.results)[0]].xAxis === "Time") { // options (time / year)
                                const minute = d * 15;
                                return `${Math.floor(minute / 60).toString().padStart(2, "0")}:${(minute % 60).toString().padStart(2, "0")}`;
                            } else {
                                return d;
                            }
                        }}
                    />

                    <ChartLabel
                        text={ this.props.results[Object.keys(this.props.results)[0]].xAxis }  // TODO: should not use the xAxis of a specified attribute 
                        className="alt-x-label"
                        includeMargin={false}
                        xPercent={0.5}
                        yPercent={1.09}
                        style={{
                            fontWeight: "bold"
                        }}
                    />

                    <ChartLabel
                        text={ this.props.results[Object.keys(this.props.results)[0]].unit }  // TODO: should not use the unit of a specified attribute 
                        className="alt-y-label"
                        includeMargin={false}
                        xPercent={0.02}
                        yPercent={0.05}
                        style={{
                            fontWeight: "bold"
                        }}
                    />

                    <YAxis
                        // title={ this.props.results[Object.keys(this.props.results)[0]].unit }
                        position="end"
                        tickLabelAngle={-70}
                    />
                </XYPlot>
            </div>
        );
    }
}

export default ResultChart;
