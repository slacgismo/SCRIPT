import React from "react";
import "../../../node_modules/react-vis/dist/style.css";
import {
    XYPlot,
    LineSeries,
    HorizontalGridLines,
    XAxis,
    YAxis,
    Borders,
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
        ];

        if (this.props.algId === 1) {
            return (
                <div className="chart-grid">
                    <XYPlot height={300} width={600}>
                        <DiscreteColorLegend
                            style={{position: "absolute", left: "50px", top: "10px"}}
                            orientation="vertical"
                            items={[
                                {
                                    title: this.props.lable_uncontrolled,
                                    color: "#12939A"
                                },
                                {
                                    title: this.props.lable_controlled,
                                    color: "#FF8000"
                                }
                            ]}
                        />
                        <HorizontalGridLines />
                        <LineSeries data={ this.props.data_uncontrolled }  color="#12939A"/>
                        <LineSeries data={ this.props.data_controlled } color="#FF8000"/>
                        <XAxis
                            title={ this.props.xAxis }
                            position="end"
                        />
                        <YAxis
                            // title={ this.props.yAxis }
                            position="end"
                        />
                    </XYPlot>
                </div>
            );
        } else if (this.props.algId === 2) {
            const { results } = this.props;
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
                    <XYPlot height={300} width={500}>
                        <DiscreteColorLegend
                            style={{
                                position: "absolute",
                                left: "520px",
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
                            title={ this.props.results["residential_l1_load"].xAxis } // TODO: should not use the xAxis of a specified attribute 
                            position="end"
                            tickFormat={function tickFormat(d){
                                const minute = d * 15;
                                return `${Math.floor(minute / 60).toString().padStart(2, "0")}:${(minute % 60).toString().padStart(2, "0")}`;
                            }}
                        />

                        <YAxis
                            // title={ this.props.yAxis }
                            position="end"
                            tickLabelAngle={-70}
                        />
                    </XYPlot>
                </div>
            );
        }

        
    }
}

export default ResultChart;
