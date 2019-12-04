import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json';
import svgPanZoom from 'svg-pan-zoom';
import OverviewMapTabs from './OverviewMapTabs';
import Button from '@material-ui/core/Button';
import TextField from "@material-ui/core/TextField";
import Select from '@material-ui/core/Select';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormHelperText from '@material-ui/core/FormHelperText';
import FormControl from '@material-ui/core/FormControl';
import { makeStyles } from "@material-ui/core/styles";

import {
  Wrapper,
  Output,
  MapWrapper,
  Tooltip,
  ParamTabs,
  getStyledMapWrapperByCountyColors,
  addCountyColorByAttr,
} from './overviewMapStyled';
import { counties } from '../Api/sampleCounties';
import OverviewMapLegend from './OverviewMapLegend';

const useStyles = makeStyles(theme => ({
    formControl: {
        margin: theme.spacing(1),
        marginLeft: theme.spacing(1.5),
        minWidth: 200,
    },
    selectEmpty: {
        marginTop: theme.spacing(2),
    },
}));

const ParamSelect = (props) => {
    const classes = useStyles();
    return (
        <>
            <FormControl className={classes.formControl}>
                <InputLabel id="overview-param-select-label">Overview Parameter</InputLabel>
                <Select
                    labelId="overview-param-select-label"
                    id="overview-param-select"
                    value={ props.overviewAttr }
                    onChange={ event => props.changeOverviewAttr(event.target.value) }
                >
                {
                    Object.keys(props.allOverviewParams).map(param => (
                        <MenuItem
                            key={ props.allOverviewParams[param].id }
                            value={ param }
                        >
                            { props.allOverviewParams[param].text }
                        </MenuItem>
                    ))
                }
                </Select>
            </FormControl>
        </>
    ) 
}

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

    if (this.state.styledMap) {
      return (
        <this.state.styledMap>
          <ParamTabs>
            <h2>Overview Map of California</h2>
            {
                <ParamSelect
                    allOverviewParams={ this.state.allOverviewParams }
                    changeOverviewAttr={ newAttr => this.changeOverviewAttr(newAttr) }
                    overviewAttr={ this.state.chosenParam }
                />
            }
            <OverviewMapLegend
                startValue="start"
                midValue="mid"
                endValue="end"
            />
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