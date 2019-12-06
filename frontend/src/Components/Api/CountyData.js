import axios from "axios";
import { serverUrl } from "./server";

let countyRes = [];
countyRes = axios.get(`${serverUrl}/county`);
export { countyRes };

// Here is a sample data of counties
// The data fetched from '/api/county/' is supposed to be like this.
const counties = [
    {
        "name": "alameda",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "alpine",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "amador",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "butte",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "calaveras",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "colusa",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "contra costa",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "del norte",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "el dorado",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "fresno",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "glenn",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "humboldt",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "imperial",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "inyo",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "kern",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "kings",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "lake",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "lassen",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "los angeles",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "madera",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "marin",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "mariposa",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "mendocino",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "merced",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "modoc",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "mono",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "monterey",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "napa",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "nevada",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "orange",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "placer",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "plumas",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "riverside",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "sacramento",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "san benito",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "san bernardino",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "san diego",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "san franciso",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "san joaquin",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "san luis obispo",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "san mateo",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "santa barbara",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "santa clara",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "santa cruz",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "shasta",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "sierra",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "siskiyou",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "solano",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "sonoma",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "stanislaus",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "sutter",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "tehama",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "trinity",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    },
    {
        "name": "tulare",
        "total_session": 96,
        "total_energy": 12829.0,
        "peak_energy": 0.15997
    },
    {
        "name": "tuolumne",
        "total_session": 96,
        "total_energy": 8965.0,
        "peak_energy": 0.16997
    },
    {
        "name": "ventura",
        "total_session": 96,
        "total_energy": 6180.0,
        "peak_energy": 0.16997
    },
    {
        "name": "yolo",
        "total_session": 96,
        "total_energy": 12368.0,
        "peak_energy": 0.16997
    },
    {
        "name": "yuba",
        "total_session": 96,
        "total_energy": 7403.0,
        "peak_energy": 0.17997
    }
];
