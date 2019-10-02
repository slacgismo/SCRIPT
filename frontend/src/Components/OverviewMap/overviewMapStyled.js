import styled from 'styled-components';
import { rgba } from 'polished';

const BORDER_STYLE = `0.2rem solid ${rgba('#000', 0.15)}`;
const STROKE_COLOR = '#fff';

export const Wrapper = styled.div`
  display: flex;
  flex-flow: nowrap row;
  @media (max-width: 600px) {
    flex-flow: nowrap column;
  }
`;

export const Output = styled.div`
  margin: 1rem;
  padding: 1rem;
  flex: 1 1 0;
  border: ${BORDER_STYLE};
  @media (max-width: 600px) {
    padding-right: 0;
    padding-bottom: 1rem;
    border-right: none;
    border-bottom: 0.2rem solid ${BORDER_STYLE};
  }
`;

export const MapWrapper = styled.div`
  padding-left: 1rem;
  flex: 1 1 auto;
  @media (max-width: 600px) {
    padding-left: 0;
    padding-top: 1rem;
  }
  svg {
    stroke: ${STROKE_COLOR};
    stroke-width: 0.1;
    stroke-linecap: round;
    stroke-linejoin: round;
    path {
      :focus {
        outline: 0;
      }
    }
  }
`;

export const Tooltip = styled.div`
  position: absolute;
  padding: 0.25rem;
  background: white;
  border: 0.2rem solid #ccc;
`;

export const getStyledMapWrapperByCountyColors = (countyColors) => {
  let countyColorsCSS = '';
  Object.keys(countyColors).forEach(county => {
    countyColorsCSS += `
      path[id='${county}'] {
        fill: ${countyColors[county]};
      }
    `
  });

  const StyledMap = styled(MapWrapper)`
    svg {
      margin: 1rem;
      padding: 1rem;
      border: ${BORDER_STYLE};
      width: 600px;
      height: 300px;
      viewBox: "500px 500px 500px 500px";

      path {
        cursor: pointer;

        &:hover {
          opacity: 0.75;
        }
      }

      ${countyColorsCSS}
    }
  `;

  return StyledMap
}
