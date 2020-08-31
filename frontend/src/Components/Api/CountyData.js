import axios from "axios";
import { serverUrl } from "./server";

console.log('SERVER URL', serverUrl)
let countyRes = [];
countyRes = axios.get(`${serverUrl}/county`);
export { countyRes };
