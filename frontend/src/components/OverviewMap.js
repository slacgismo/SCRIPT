import React from 'react';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json';

class OverviewMap extends React.Component {
  render () {
    return (
      <VectorMap { ...caMapData } />
    )
  }
}

export default OverviewMap;