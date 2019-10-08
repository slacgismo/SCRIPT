import React, {Component} from 'react';
import Base from '../../Layouts/Base'
import Content from '../../Layouts/Content'

class Overview extends Component {
  render() {
    return (
      <div >
        <Base content={<Content text={'OveviewMap'}/>}/>
      </div>
    );
  }
}

export default Overview;