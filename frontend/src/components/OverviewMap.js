import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json'
import { Wrapper, Output, MapWrapper } from './overviewMapStyled';

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

const Tooltip = styled.div`
  position: absolute;
  padding: 0.25rem;
  background: white;
  border: 0.2rem solid #ccc;
`;

class OverviewMap extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      current: null,
      isTooltipVisible: false,
      tooltipY: 0,
      tooltipX: 0,
    };
  }

  onMouseOver = e => {
    this.setState({ current: e.target.attributes.name.value });
  }

  onMouseMove = e => {
    this.setState({
      isTooltipVisible: true,
      tooltipY: e.pageY + 10,
      tooltipX: e.pageX + 10,
    })
  }

  onMouseOut = () => {
    this.setState({ current: null, isTooltipVisible: false });
  }

  render () {
    const { current, isTooltipVisible, tooltipX, tooltipY } = this.state;
    
    const layerProps = {
      onMouseOver: this.onMouseOver,
      onMouseMove: this.onMouseMove,
      onMouseOut: this.onMouseOut,
    };

    const tooltipStyle = {
      display: isTooltipVisible ? 'block' : 'none',
      top: tooltipY,
      left: tooltipX,
    };

    return (
      <Wrapper
        style={{ width: "600px" }}
      >
        <StyledMap>
          <VectorMap
            { ...caMapData }
            layerProps={ layerProps } 
          />
          <Tooltip style={tooltipStyle}>{ current }</Tooltip>
        </StyledMap>
      </Wrapper>
    )
  }
}

export default OverviewMap;