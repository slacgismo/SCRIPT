import axios from "axios";
import { serverUrl } from './server'

let countyRes = [];

function fetchCounty() {
    countyRes = axios.get(`${serverUrl}/county`);
}

fetchCounty();

export { countyRes };