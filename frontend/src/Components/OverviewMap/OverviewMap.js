import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json'
import svgPanZoom from 'svg-pan-zoom'

import {
  Wrapper,
  Output,
  MapWrapper,
  Tooltip,
  getStyledMapWrapperByCountyColors,
} from './overviewMapStyled';
import { countyColors } from './sampleCountyColors';


class OverviewMap extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      current: null,
      isTooltipVisible: false,
      tooltipY: 0,
      tooltipX: 0,
    };

    this.StyledMap = getStyledMapWrapperByCountyColors(
      countyColors,
    );
    this.Viewer = null
  }

  componentDidMount() {
    const panZoomTiger = svgPanZoom('#usa-ca');
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
      <this.StyledMap>
        <VectorMap
          id={"overview-map"}
          { ...caMapData }
          layerProps={ layerProps } 
        />
        <Tooltip style={tooltipStyle}>{ current }</Tooltip>
      </this.StyledMap>
    )
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
}

export default OverviewMap;