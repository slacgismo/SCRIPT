import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json';
import svgPanZoom from 'svg-pan-zoom';
import OverviewMapTabs from './OverviewMapTabs';
import Button from '@material-ui/core/Button';

import {
  Wrapper,
  Output,
  MapWrapper,
  Tooltip,
  ParamTabs,
  getStyledMapWrapperByCountyColors,
  addCountyColorByAttr,
} from './overviewMapStyled';
import { counties } from './sampleCounties';


class OverviewMap extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      allOverviewParams: {
        totalEnergy: {
          text: 'Total Energy',
        },
        totalSession: {
          text: 'Total # of Session',
        },
      },
      chosenParam: "totalEnergy",
      current: {
        countyName: null,
        totalEnergy: null,
        totalSession: null,
      },
      isTooltipVisible: false,
      tooltipY: 0,
      tooltipX: 0,
      gotPan: false,
      styledMap: null,
    };

    // addCountyColorByAttr(counties, this.props.overviewParam);

    // this.styledMap = getStyledMapWrapperByCountyColors(
    //   counties,
    // )
    this.Viewer = null

    this.updateMap = this.updateMap.bind(this);
  }

  changeOverviewAttr(newAttr) {
      this.setState({
          chosenParam: newAttr,
      })
      this.updateMap(newAttr)
  }

  updateMap(newAttr) {
    addCountyColorByAttr(counties, newAttr);
    this.setState({
      styledMap: getStyledMapWrapperByCountyColors(counties)
    });
  }

  componentDidMount() {
    this.updateMap("totalEnergy");
  }

  componentDidUpdate() {
    if (!this.state.gotPan) {
      const panZoomTiger = svgPanZoom('#usa-ca');
      this.setState({
        gotPan: true,
      })

      console.log("got pan")
    }
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

    const paramButtons = Object.keys(this.state.allOverviewParams).map(param => (
      <Button
        className={ this.state.chosenParam == param ? "chosen" : "" }
        onClick={ () => this.changeOverviewAttr(param) }
      >
          { this.state.allOverviewParams[param].text }
      </Button>
    ))

    console.log(paramButtons)

    if (this.state.styledMap) {
      return (
        <this.state.styledMap>
          <ParamTabs>
            { paramButtons }
          </ParamTabs>
          <VectorMap
            id={"overview-map"}
            { ...caMapData }
            layerProps={ layerProps } 
          />
          <Tooltip style={tooltipStyle}>
            <b>County:</b> { current.countyName }
            <br />
            <b>Value:</b> { current[this.props.overviewParam] }
          </Tooltip>
        </this.state.styledMap>
      )
    } else {
      return <></>
    }
    
  }

  onMouseOver = e => {
    this.setState({ current: {
      countyName: e.target.attributes.name.value,
      [this.props.overviewParam]: (counties[e.target.attributes.id.value][this.props.overviewParam] * 1000).toFixed(1),
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
      [this.props.overviewParam]: null,
    }, isTooltipVisible: false });
  }
}

export default OverviewMap;