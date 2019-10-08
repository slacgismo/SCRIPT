import React from 'react';
import '../../../node_modules/react-vis/dist/style.css';
import {
  XYPlot,
  LineSeries,
  HorizontalGridLines,
  XAxis,
  YAxis,
  Borders,
} from 'react-vis';

class ResultChart extends React.Component {
  constructor(props) {
    super(props);
  }

  render() {
    const data = [
      {x: 0, y: 3},
      {x: 1, y: 5},
      {x: 2, y: 10},
      {x: 3, y: 9},
      {x: 4, y: 13},
      {x: 5, y: 15},
      {x: 6, y: 10},
      {x: 7, y: 3},
      {x: 8, y: 4},
      {x: 9, y: 5}
    ];
    return (
      <div className="App">
        <XYPlot height={300} width={300}>
          {/* <HorizontalGridLines /> */}
          <LineSeries data={data} />
          <XAxis
            title="Time"
            position="end"
          />
          <YAxis
            title="Energy"
            position="end"
          />
          <Borders style={{
            bottom: {fill: '#fff'},
            left: {fill: '#fff'},
            right: {fill: '#fff'},
            top: {fill: '#fff'}
          }}/>
        </XYPlot>
      </div>
    );
  }
}

export default ResultChart;