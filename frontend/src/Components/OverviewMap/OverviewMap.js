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
            id: 'total-energy',
            text: 'Total Energy',
        },
        totalSession: {
            id: 'total-session-num',
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
      });
      this.updateMap(newAttr);
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
    const panZoomMap = svgPanZoom('#usa-ca');
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

    const paramSelect = (
        <form noValidate autoComplete="off">
            <TextField
                id="standart-county"
                select
                className={classes.textField}
                SelectProps={{
                    native: true,
                    MenuProps: {
                        className: classes.menu,
                    },
                }}
                helperText="Please select your county"  
                margin="normal"
            >
                {
                    Object.keys(this.state.allOverviewParams).map(param => (
                        <option
                            key={ this.state.allOverviewParams[param].id }
                            value={ this.state.allOverviewParams[param].id }
                        >
                            { this.state.allOverviewParams[param].text }
                        </option>
                    ))
                }
            </TextField>
            <p/>
            <Button variant="contained" color="primary" className={classes.button} onClick={runAlgorithm2}>
                Run
            </Button>
        </form> 
    )

    if (this.state.styledMap) {
      return (
        <this.state.styledMap>
          <ParamTabs>
            <h2>Overview Map of California</h2>
            { paramSelect }
          </ParamTabs>
          <VectorMap
            id={"overview-map"}
            { ...caMapData }
            layerProps={ layerProps } 
          />
          <Tooltip style={tooltipStyle}>
            <b>County:</b> { current.countyName }
            <br />
            <b>{ this.state.allOverviewParams[this.state.chosenParam].text }:</b> { current[this.state.chosenParam] }
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
      [this.state.chosenParam]: (counties[e.target.attributes.id.value][this.state.chosenParam] * 1000).toFixed(1),
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
      [this.state.chosenParam]: null,
    }, isTooltipVisible: false });
  }
}

export default OverviewMap;