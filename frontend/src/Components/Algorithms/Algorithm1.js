import React, {Component} from 'react';
import Base from '../../Layouts/Base';
import Content from '../../Layouts/Content';
import Scenario from './Scenario';
import ResultCharts from '../ResultChart/ResultCharts';

class Algorithm1 extends Component {
  render() {
    return (
      <div >
        <Base 
        content={
        <div>
        <Content text={'Scenario'} compo={<Scenario />}/> 
        <br/>
        <Content text={'Results'} compo={ <ResultCharts />} />
        </div>
        }/>
      </div>
    );
  }
}

export default Algorithm1;