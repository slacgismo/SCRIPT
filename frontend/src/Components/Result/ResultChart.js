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
        const newItems = [];
        const newData = [];
        Object.keys(results).forEach((attr, i) => {
            console.log("LOOK AT ME", results)
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
                {
                    /* title of chart */
                    this.props.legendPosition === "none" &&
                    <h5 className='chartTitle'>{ Object.keys(results)[0] }</h5>
                }

                {/* X Axis Label */}
                <h5 className='chartXLabel'>{ this.props.results[Object.keys(this.props.results)[0]].xAxis }</h5>

                <XYPlot height={ this.props.graphHeight } width={ this.props.graphWidth }>
                    {
                        this.props.legendPosition === "right" &&
                        <DiscreteColorLegend
                            style={{
                                position: "absolute",
                                left: this.props.graphWidth + 40,
                                top: "15px",
                                width: "13rem",
                            }}
                            orientation="vertical"
                            items={ newItems }
                        />
                    }
                    
                            
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

                    {/* <ChartLabel
                        text={ this.props.results[Object.keys(this.props.results)[0]].xAxis }  // TODO: should not use the xAxis of a specified attribute 
                        className="alt-x-label"
                        includeMargin={false}
                        xPercent={0.5}
                        yPercent={1.09}
                        style={{
                            fontWeight: "bold"
                        }}
                    /> */}

                    {
                        this.props.legendPosition !== "none" &&
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
                    }

                    <YAxis
                        // title={ this.props.results[Object.keys(this.props.results)[0]].unit }
                        position="end"
                        tickLabelAngle={ -70 }
                        tickTotal={ 4 }
                        tickFormat={(d) => {
                            if (d >= Math.pow(10, 15)) {
                                return `${d / Math.pow(10, 15)}P`;
                            } else if (d >= Math.pow(10, 12)) {
                                return `${d / Math.pow(10, 12)}T`;
                            } else if (d >= Math.pow(10, 9)) {
                                return `${d / Math.pow(10, 9)}G`;
                            } else if (d >= Math.pow(10, 6)) {
                                return `${d / Math.pow(10, 6)}M`;
                            } else if (d >= Math.pow(10, 3)) {
                                return `${d / Math.pow(10, 3)}K`;
                            } else {
                                return d;
                            }
                        }}
                    />
                </XYPlot>
            </div>
        );
    }
}

export default ResultChart;
