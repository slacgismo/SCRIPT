import React from 'react';
import PropTypes from 'prop-types';
import styled from 'styled-components';
import VectorMap from '@south-paw/react-vector-maps';
import caMapData from '@south-paw/react-vector-maps/maps/json/usa-ca.json'
import { Wrapper, Output, MapWrapper } from './overviewMapStyled';

class OverviewMap extends React.PureComponent {
  constructor(props) {
    super(props);

    this.state = {
      current: null,
      isTooltipVisible: false,
      tooltipY: 0,
      tooltipX: 0,

      countyColors: {
        'santa clara': '#ed3f00',
        'san mateo': '#243ed4',
      },
    };

    const countyColors = this.state.countyColors;
    let countyColorsCSS = '';
    Object.keys(countyColors).forEach(county => {
      countyColorsCSS += `
        path[id='${county}'] {
          fill: ${countyColors[county]};
        }
      `
    });

    this.StyledMap = styled(MapWrapper)`
      svg {
        path {
          cursor: pointer;

          &:hover {
            opacity: 0.75;
          }
        }

        ${countyColorsCSS}
      }
    `;

    this.Tooltip = styled.div`
      position: absolute;
      padding: 0.25rem;
      background: white;
      border: 0.2rem solid #ccc;
    `;
  }

  componentDidMount() {
    // this.addColorToRegions();
  }

  // TODO: Seek for better practice
  addColorToRegions() {
    const countyColors = this.state.countyColors;
    Object.keys(countyColors).forEach(county => {
      document.getElementById(`#${ county }`).style.fill = countyColors[county]
    })
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
        <this.StyledMap>
          <VectorMap
            { ...caMapData }
            layerProps={ layerProps } 
          />
          <this.Tooltip style={tooltipStyle}>{ current }</this.Tooltip>
        </this.StyledMap>
      </Wrapper>
    )
  }
}

export default OverviewMap;