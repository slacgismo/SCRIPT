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
        // Fake data
        //
        // const data = [
        //     {x: 1, y: 8},
        //     {x: 2, y: 10},
        //     {x: 3, y: 9},
        //     {x: 4, y: 13},
        //     {x: 5, y: 15},
        //     {x: 6, y: 10},
        //     {x: 7, y: 12},
        //     {x: 8, y: 10},
        //     {x: 9, y: 11},
        //     {x: 10, y: 12},
        //     {x: 11, y: 9},
        //     {x: 12, y: 8},
        // ];

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
            return (
                <div className="chart-grid">
                    <XYPlot height={300} width={500}>
                        <DiscreteColorLegend
                            style={{
                                position: "absolute",
                                left: "520px",
                                top: "15px",
                                width: '30rem',
                            }}
                            orientation="vertical"
                            items={[
                                {
                                    title: this.props.label_r1,
                                    color: "#e62020"
                                },
                                {
                                    title: this.props.label_r2,
                                    color: "#e3b920"
                                },
                                {
                                    title: this.props.label_rm,
                                    color: "#63b81a"
                                },
                                {
                                    title: this.props.label_work,
                                    color: "#25c3db"
                                },
                                {
                                    title: this.props.label_fast,
                                    color: "#3b22e0"
                                },
                                {
                                    title: this.props.label_p2,
                                    color: "#c921db"
                                },
                                {
                                    title: this.props.label_total,
                                    color: "#911955"
                                }
                            ]}
                        />
                        <HorizontalGridLines />
                        
                        <LineSeries data={ this.props.data_r1 }  color="#e62020" strokeWidth="1px"/>
                        <LineSeries data={ this.props.data_r2 } color="#e3b920"/>
                        <LineSeries data={ this.props.data_rm } color="#63b81a"/>
                        <LineSeries data={ this.props.data_work } color="#25c3db"/>
                        <LineSeries data={ this.props.data_fast } color="#3b22e0"/>
                        <LineSeries data={ this.props.data_p2 } color="#c921db"/>
                        <LineSeries data={ this.props.data_total } color="#911955"/>
                        
                        <XAxis
                            title={ this.props.xAxis }
                            position="end"
                            tickFormat={function tickFormat(d){
                                const minute = d * 15
                                return `${Math.floor(minute / 60).toString().padStart(2, '0')}:${(minute % 60).toString().padStart(2, '0')}`
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