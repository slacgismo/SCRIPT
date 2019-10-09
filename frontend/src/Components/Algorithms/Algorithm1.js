import React, {Component} from 'react';
import Base from '../../Layouts/Base';
import Content from '../../Layouts/Content';
import Scenario from './Scenario';
import ResultCharts from '../ResultChart/ResultCharts';

class Algorithm1 extends Component {
  constructor(props) {
    super(props);
    this.state = {
      status: "pending", // "pending" / "running" / "finished"
    }
  }

  changeStatus(newStatus) {
    this.setState({
      status: newStatus,
    });
  }

  render() {
    return (
      <div>
        <Base 
        content={
        <div>
        <Content
          text={'Scenario'}
          compo={
            <Scenario changeStatus={this.changeStatus.bind(this)} />
          }
        /> 
        <br/>
        {
          this.state.status === "finished" &&
          <Content text={'Results'} compo={ <ResultCharts />} />
        }
        </div>
        }/>
      </div>
    );
  }
}

export default Algorithm1;