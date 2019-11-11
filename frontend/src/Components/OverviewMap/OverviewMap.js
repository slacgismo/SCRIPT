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
  addCountyColorByAttr,
} from './overviewMapStyled';
import { counties } from './sampleCounties';


class OverviewMap extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      current: {
        countyName: null,
        totalEnergy: null,
        totalSession: null,
      },
      isTooltipVisible: false,
      tooltipY: 0,
      tooltipX: 0,
      overviewParam: 'totalEnergy',
    };

    addCountyColorByAttr(counties, this.state.overviewParam);

    this.StyledMap = getStyledMapWrapperByCountyColors(
      counties,
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
      width: '15rem',
    };

    return (
      <this.StyledMap>
        <VectorMap
          id={"overview-map"}
          { ...caMapData }
          layerProps={ layerProps } 
        />
        <Tooltip style={tooltipStyle}>
          <b>County:</b> { current.countyName }
          <br />
          <b>Value:</b> { current[this.state.overviewParam] }
        </Tooltip>
      </this.StyledMap>
    )
  }

  onMouseOver = e => {
    this.setState({ current: {
      countyName: e.target.attributes.name.value,
      [this.state.overviewParam]: (counties[e.target.attributes.id.value][this.state.overviewParam] * 1000).toFixed(1),
    } });
  }

  onMouseMove = e => {
    this.setState({
      isTooltipVisible: true,
      tooltipY: e.pageY + 10,
      tooltipX: e.pageX + 10,
    })
  }

  onMouseOut = () => {
    this.setState({ current: {
      countyName: null,
      [this.state.overviewParam]: null,
    }, isTooltipVisible: false });
  }
}

export default OverviewMap;