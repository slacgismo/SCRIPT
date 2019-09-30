import React from 'react';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json'
import { Wrapper, Output, MapWrapper } from './overviewMapStyled';

class OverviewMap extends React.Component {
  render () {
    const StyledMap = styled(MapWrapper)`
      svg {
        path {
          fill: #3d0043;
          cursor: pointer;

          &:hover {
            fill: #90007f;
          }

          &[aria-current='true'] {
            fill: #d52484;
          }
        }
      }
    `;

    return (
      <StyledMap>
        <VectorMap
          style={{ width: "30%" }} // TODO: remove this line
          { ...caMapData }
        />
      </StyledMap>
    )
  }
}

export default OverviewMap;