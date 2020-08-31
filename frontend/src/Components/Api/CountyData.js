import axios from "axios";
import { serverUrl } from "./server";

let countyRes = [];
countyRes = axios.get(`${serverUrl}/county`);
export { countyRes };
