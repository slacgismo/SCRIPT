// Sample of fetching data
//
// const respResults = await axios.get("http://127.0.0.1:8000/api/algorithm/load_controller/");
//
// let uncontrolledLoad = JSON.parse(respResults.data[0].uncontrolled_load);
// let controlledLoad = JSON.parse(respResults.data[0].controlled_load);
//
// console.log(uncontrolledLoad);
// console.log(controlledLoad);

export const dataLoadControll = [{
    uncontrolled_load: "[{\"time\": \"0:00\", \"load\": \"6634.6\"}, {\"time\": \"1:15\", \"load\": \"6598.8\"}, {\"time\": \"2:30\", \"load\": \"6576.4\"}, {\"time\": \"3:45\", \"load\": \"6559.4\"}, {\"time\": \"0:00\", \"load\": \"6486.0\"}, {\"time\": \"1:15\", \"load\": \"6420.6\"}, {\"time\": \"2:30\", \"load\": \"6326.2\"}, {\"time\": \"3:45\", \"load\": \"6233.8\"}, {\"time\": \"0:00\", \"load\": \"6102.8\"}, {\"time\": \"1:15\", \"load\": \"5959.0\"}, {\"time\": \"2:30\", \"load\": \"5794.6\"}, {\"time\": \"3:45\", \"load\": \"5600.0\"}, {\"time\": \"0:00\", \"load\": \"5378.8\"}, {\"time\": \"1:15\", \"load\": \"5144.2\"}, {\"time\": \"2:30\", \"load\": \"4876.2\"}, {\"time\": \"3:45\", \"load\": \"4620.2\"}, {\"time\": \"0:00\", \"load\": \"4347.8\"}, {\"time\": \"1:15\", \"load\": \"4080.0\"}, {\"time\": \"2:30\", \"load\": \"3784.8\"}, {\"time\": \"3:45\", \"load\": \"3478.0\"}, {\"time\": \"0:00\", \"load\": \"3208.6\"}, {\"time\": \"1:15\", \"load\": \"2953.2\"}, {\"time\": \"2:30\", \"load\": \"2741.8\"}, {\"time\": \"3:45\", \"load\": \"2575.6\"}, {\"time\": \"0:00\", \"load\": \"2383.2\"}, {\"time\": \"1:15\", \"load\": \"2224.6\"}, {\"time\": \"2:30\", \"load\": \"2088.2\"}, {\"time\": \"3:45\", \"load\": \"1955.4\"}, {\"time\": \"0:00\", \"load\": \"1867.4\"}, {\"time\": \"1:15\", \"load\": \"1814.4\"}, {\"time\": \"2:30\", \"load\": \"1770.6\"}, {\"time\": \"3:45\", \"load\": \"1754.4\"}, {\"time\": \"0:00\", \"load\": \"1755.8\"}, {\"time\": \"1:15\", \"load\": \"1760.6\"}, {\"time\": \"2:30\", \"load\": \"1774.2\"}, {\"time\": \"3:45\", \"load\": \"1785.4\"}, {\"time\": \"0:00\", \"load\": \"1816.0\"}, {\"time\": \"1:15\", \"load\": \"1850.4\"}, {\"time\": \"2:30\", \"load\": \"1901.0\"}, {\"time\": \"3:45\", \"load\": \"1953.4\"}, {\"time\": \"0:00\", \"load\": \"1998.4\"}, {\"time\": \"1:15\", \"load\": \"2052.0\"}, {\"time\": \"2:30\", \"load\": \"2076.8\"}, {\"time\": \"3:45\", \"load\": \"2101.0\"}, {\"time\": \"0:00\", \"load\": \"2138.4\"}, {\"time\": \"1:15\", \"load\": \"2158.4\"}, {\"time\": \"2:30\", \"load\": \"2191.8\"}, {\"time\": \"3:45\", \"load\": \"2215.8\"}, {\"time\": \"0:00\", \"load\": \"2249.0\"}, {\"time\": \"1:15\", \"load\": \"2265.8\"}, {\"time\": \"2:30\", \"load\": \"2303.2\"}, {\"time\": \"3:45\", \"load\": \"2316.6\"}, {\"time\": \"0:00\", \"load\": \"2338.4\"}, {\"time\": \"1:15\", \"load\": \"2358.2\"}, {\"time\": \"2:30\", \"load\": \"2388.8\"}, {\"time\": \"3:45\", \"load\": \"2419.0\"}, {\"time\": \"0:00\", \"load\": \"2437.6\"}, {\"time\": \"1:15\", \"load\": \"2456.0\"}, {\"time\": \"2:30\", \"load\": \"2470.0\"}, {\"time\": \"3:45\", \"load\": \"2488.4\"}, {\"time\": \"0:00\", \"load\": \"2519.4\"}, {\"time\": \"1:15\", \"load\": \"2529.4\"}, {\"time\": \"2:30\", \"load\": \"2553.4\"}, {\"time\": \"3:45\", \"load\": \"2571.6\"}, {\"time\": \"0:00\", \"load\": \"2570.6\"}, {\"time\": \"1:15\", \"load\": \"2598.8\"}, {\"time\": \"2:30\", \"load\": \"2622.8\"}, {\"time\": \"3:45\", \"load\": \"2673.8\"}, {\"time\": \"0:00\", \"load\": \"2738.6\"}, {\"time\": \"1:15\", \"load\": \"2833.0\"}, {\"time\": \"2:30\", \"load\": \"3010.4\"}, {\"time\": \"3:45\", \"load\": \"3187.2\"}, {\"time\": \"0:00\", \"load\": \"3406.8\"}, {\"time\": \"1:15\", \"load\": \"3618.8\"}, {\"time\": \"2:30\", \"load\": \"3827.8\"}, {\"time\": \"3:45\", \"load\": \"4049.8\"}, {\"time\": \"0:00\", \"load\": \"4233.4\"}, {\"time\": \"1:15\", \"load\": \"4390.0\"}, {\"time\": \"2:30\", \"load\": \"4569.0\"}, {\"time\": \"3:45\", \"load\": \"4681.6\"}, {\"time\": \"0:00\", \"load\": \"4811.2\"}, {\"time\": \"1:15\", \"load\": \"4903.8\"}, {\"time\": \"2:30\", \"load\": \"5041.2\"}, {\"time\": \"3:45\", \"load\": \"5209.0\"}, {\"time\": \"0:00\", \"load\": \"5350.4\"}, {\"time\": \"1:15\", \"load\": \"5515.8\"}, {\"time\": \"2:30\", \"load\": \"5703.2\"}, {\"time\": \"3:45\", \"load\": \"5863.8\"}, {\"time\": \"0:00\", \"load\": \"6036.4\"}, {\"time\": \"1:15\", \"load\": \"6234.0\"}, {\"time\": \"2:30\", \"load\": \"6349.4\"}, {\"time\": \"3:45\", \"load\": \"6496.4\"}, {\"time\": \"0:00\", \"load\": \"6561.2\"}, {\"time\": \"1:15\", \"load\": \"6602.4\"}, {\"time\": \"2:30\", \"load\": \"6619.4\"}, {\"time\": \"3:45\", \"load\": \"6628.2\"}]",
    controlled_load: "[{\"time\": \"0:00\", \"load\": \"3531.8\"}, {\"time\": \"1:15\", \"load\": \"2741.4\"}, {\"time\": \"2:30\", \"load\": \"2175.0\"}, {\"time\": \"3:45\", \"load\": \"1735.8\"}, {\"time\": \"0:00\", \"load\": \"1398.4\"}, {\"time\": \"1:15\", \"load\": \"1139.2\"}, {\"time\": \"2:30\", \"load\": \"927.8\"}, {\"time\": \"3:45\", \"load\": \"746.6\"}, {\"time\": \"0:00\", \"load\": \"676.6\"}, {\"time\": \"1:15\", \"load\": \"597.4\"}, {\"time\": \"2:30\", \"load\": \"530.6\"}, {\"time\": \"3:45\", \"load\": \"506.6\"}, {\"time\": \"0:00\", \"load\": \"355.0\"}, {\"time\": \"1:15\", \"load\": \"305.6\"}, {\"time\": \"2:30\", \"load\": \"248.8\"}, {\"time\": \"3:45\", \"load\": \"201.6\"}, {\"time\": \"0:00\", \"load\": \"137.6\"}, {\"time\": \"1:15\", \"load\": \"144.2\"}, {\"time\": \"2:30\", \"load\": \"176.0\"}, {\"time\": \"3:45\", \"load\": \"244.2\"}, {\"time\": \"0:00\", \"load\": \"331.8\"}, {\"time\": \"1:15\", \"load\": \"391.6\"}, {\"time\": \"2:30\", \"load\": \"523.6\"}, {\"time\": \"3:45\", \"load\": \"661.2\"}, {\"time\": \"0:00\", \"load\": \"861.4\"}, {\"time\": \"1:15\", \"load\": \"1056.2\"}, {\"time\": \"2:30\", \"load\": \"1399.2\"}, {\"time\": \"3:45\", \"load\": \"1798.2\"}, {\"time\": \"0:00\", \"load\": \"2123.6\"}, {\"time\": \"1:15\", \"load\": \"2490.2\"}, {\"time\": \"2:30\", \"load\": \"2819.0\"}, {\"time\": \"3:45\", \"load\": \"3144.6\"}, {\"time\": \"0:00\", \"load\": \"3527.2\"}, {\"time\": \"1:15\", \"load\": \"3866.4\"}, {\"time\": \"2:30\", \"load\": \"4150.0\"}, {\"time\": \"3:45\", \"load\": \"4353.4\"}, {\"time\": \"0:00\", \"load\": \"4602.0\"}, {\"time\": \"1:15\", \"load\": \"4721.4\"}, {\"time\": \"2:30\", \"load\": \"4862.0\"}, {\"time\": \"3:45\", \"load\": \"4933.6\"}, {\"time\": \"0:00\", \"load\": \"4882.2\"}, {\"time\": \"1:15\", \"load\": \"4966.6\"}, {\"time\": \"2:30\", \"load\": \"4872.0\"}, {\"time\": \"3:45\", \"load\": \"4815.0\"}, {\"time\": \"0:00\", \"load\": \"4712.8\"}, {\"time\": \"1:15\", \"load\": \"4544.2\"}, {\"time\": \"2:30\", \"load\": \"4430.4\"}, {\"time\": \"3:45\", \"load\": \"4181.4\"}, {\"time\": \"0:00\", \"load\": \"3987.6\"}, {\"time\": \"1:15\", \"load\": \"3836.0\"}, {\"time\": \"2:30\", \"load\": \"3791.8\"}, {\"time\": \"3:45\", \"load\": \"3664.2\"}, {\"time\": \"0:00\", \"load\": \"3547.4\"}, {\"time\": \"1:15\", \"load\": \"3320.0\"}, {\"time\": \"2:30\", \"load\": \"3122.0\"}, {\"time\": \"3:45\", \"load\": \"2852.4\"}, {\"time\": \"0:00\", \"load\": \"2726.2\"}, {\"time\": \"1:15\", \"load\": \"2672.8\"}, {\"time\": \"2:30\", \"load\": \"2528.2\"}, {\"time\": \"3:45\", \"load\": \"2320.0\"}, {\"time\": \"0:00\", \"load\": \"2146.8\"}, {\"time\": \"1:15\", \"load\": \"2147.0\"}, {\"time\": \"2:30\", \"load\": \"2057.2\"}, {\"time\": \"3:45\", \"load\": \"2060.2\"}, {\"time\": \"0:00\", \"load\": \"2062.0\"}, {\"time\": \"1:15\", \"load\": \"2188.8\"}, {\"time\": \"2:30\", \"load\": \"2601.6\"}, {\"time\": \"3:45\", \"load\": \"3044.4\"}, {\"time\": \"0:00\", \"load\": \"3611.8\"}, {\"time\": \"1:15\", \"load\": \"4237.8\"}, {\"time\": \"2:30\", \"load\": \"4896.2\"}, {\"time\": \"3:45\", \"load\": \"5577.6\"}, {\"time\": \"0:00\", \"load\": \"6341.0\"}, {\"time\": \"1:15\", \"load\": \"7130.0\"}, {\"time\": \"2:30\", \"load\": \"7785.8\"}, {\"time\": \"3:45\", \"load\": \"8147.6\"}, {\"time\": \"0:00\", \"load\": \"8314.0\"}, {\"time\": \"1:15\", \"load\": \"8621.2\"}, {\"time\": \"2:30\", \"load\": \"8719.2\"}, {\"time\": \"3:45\", \"load\": \"8800.0\"}, {\"time\": \"0:00\", \"load\": \"8637.4\"}, {\"time\": \"1:15\", \"load\": \"8373.8\"}, {\"time\": \"2:30\", \"load\": \"8269.2\"}, {\"time\": \"3:45\", \"load\": \"8232.6\"}, {\"time\": \"0:00\", \"load\": \"7972.4\"}, {\"time\": \"1:15\", \"load\": \"8116.4\"}, {\"time\": \"2:30\", \"load\": \"8231.4\"}, {\"time\": \"3:45\", \"load\": \"8387.2\"}, {\"time\": \"0:00\", \"load\": \"8071.8\"}, {\"time\": \"1:15\", \"load\": \"7824.0\"}, {\"time\": \"2:30\", \"load\": \"7389.8\"}, {\"time\": \"3:45\", \"load\": \"6754.2\"}, {\"time\": \"0:00\", \"load\": \"5969.0\"}, {\"time\": \"1:15\", \"load\": \"5317.8\"}, {\"time\": \"2:30\", \"load\": \"4567.6\"}, {\"time\": \"3:45\", \"load\": \"3861.2\"}]",
}];

export const dataLoadForecast = [{
    // id: 1,
    // aggregation_level: "county",
    // num_evs: 1000000,
    // choice: "Santa Clara",
    // fast_percent: 0.1,
    // work_percent: 0.2,
    // res_percent: 0.7,
    // l1_percent: 0.5,
    // public_l2_percent: 0.0,

    residential_l1_load: "[{\"time\": \"0:00\", \"load\": \"6634.6\"}, {\"time\": \"1:15\", \"load\": \"6598.8\"}, {\"time\": \"2:30\", \"load\": \"6576.4\"}, {\"time\": \"3:45\", \"load\": \"6559.4\"}, {\"time\": \"0:00\", \"load\": \"6486.0\"}, {\"time\": \"1:15\", \"load\": \"6420.6\"}, {\"time\": \"2:30\", \"load\": \"6326.2\"}, {\"time\": \"3:45\", \"load\": \"6233.8\"}, {\"time\": \"0:00\", \"load\": \"6102.8\"}, {\"time\": \"1:15\", \"load\": \"5959.0\"}, {\"time\": \"2:30\", \"load\": \"5794.6\"}, {\"time\": \"3:45\", \"load\": \"5600.0\"}, {\"time\": \"0:00\", \"load\": \"5378.8\"}, {\"time\": \"1:15\", \"load\": \"5144.2\"}, {\"time\": \"2:30\", \"load\": \"4876.2\"}, {\"time\": \"3:45\", \"load\": \"4620.2\"}, {\"time\": \"0:00\", \"load\": \"4347.8\"}, {\"time\": \"1:15\", \"load\": \"4080.0\"}, {\"time\": \"2:30\", \"load\": \"3784.8\"}, {\"time\": \"3:45\", \"load\": \"3478.0\"}, {\"time\": \"0:00\", \"load\": \"3208.6\"}, {\"time\": \"1:15\", \"load\": \"2953.2\"}, {\"time\": \"2:30\", \"load\": \"2741.8\"}, {\"time\": \"3:45\", \"load\": \"2575.6\"}, {\"time\": \"0:00\", \"load\": \"2383.2\"}, {\"time\": \"1:15\", \"load\": \"2224.6\"}, {\"time\": \"2:30\", \"load\": \"2088.2\"}, {\"time\": \"3:45\", \"load\": \"1955.4\"}, {\"time\": \"0:00\", \"load\": \"1867.4\"}, {\"time\": \"1:15\", \"load\": \"1814.4\"}, {\"time\": \"2:30\", \"load\": \"1770.6\"}, {\"time\": \"3:45\", \"load\": \"1754.4\"}, {\"time\": \"0:00\", \"load\": \"1755.8\"}, {\"time\": \"1:15\", \"load\": \"1760.6\"}, {\"time\": \"2:30\", \"load\": \"1774.2\"}, {\"time\": \"3:45\", \"load\": \"1785.4\"}, {\"time\": \"0:00\", \"load\": \"1816.0\"}, {\"time\": \"1:15\", \"load\": \"1850.4\"}, {\"time\": \"2:30\", \"load\": \"1901.0\"}, {\"time\": \"3:45\", \"load\": \"1953.4\"}, {\"time\": \"0:00\", \"load\": \"1998.4\"}, {\"time\": \"1:15\", \"load\": \"2052.0\"}, {\"time\": \"2:30\", \"load\": \"2076.8\"}, {\"time\": \"3:45\", \"load\": \"2101.0\"}, {\"time\": \"0:00\", \"load\": \"2138.4\"}, {\"time\": \"1:15\", \"load\": \"2158.4\"}, {\"time\": \"2:30\", \"load\": \"2191.8\"}, {\"time\": \"3:45\", \"load\": \"2215.8\"}, {\"time\": \"0:00\", \"load\": \"2249.0\"}, {\"time\": \"1:15\", \"load\": \"2265.8\"}, {\"time\": \"2:30\", \"load\": \"2303.2\"}, {\"time\": \"3:45\", \"load\": \"2316.6\"}, {\"time\": \"0:00\", \"load\": \"2338.4\"}, {\"time\": \"1:15\", \"load\": \"2358.2\"}, {\"time\": \"2:30\", \"load\": \"2388.8\"}, {\"time\": \"3:45\", \"load\": \"2419.0\"}, {\"time\": \"0:00\", \"load\": \"2437.6\"}, {\"time\": \"1:15\", \"load\": \"2456.0\"}, {\"time\": \"2:30\", \"load\": \"2470.0\"}, {\"time\": \"3:45\", \"load\": \"2488.4\"}, {\"time\": \"0:00\", \"load\": \"2519.4\"}, {\"time\": \"1:15\", \"load\": \"2529.4\"}, {\"time\": \"2:30\", \"load\": \"2553.4\"}, {\"time\": \"3:45\", \"load\": \"2571.6\"}, {\"time\": \"0:00\", \"load\": \"2570.6\"}, {\"time\": \"1:15\", \"load\": \"2598.8\"}, {\"time\": \"2:30\", \"load\": \"2622.8\"}, {\"time\": \"3:45\", \"load\": \"2673.8\"}, {\"time\": \"0:00\", \"load\": \"2738.6\"}, {\"time\": \"1:15\", \"load\": \"2833.0\"}, {\"time\": \"2:30\", \"load\": \"3010.4\"}, {\"time\": \"3:45\", \"load\": \"3187.2\"}, {\"time\": \"0:00\", \"load\": \"3406.8\"}, {\"time\": \"1:15\", \"load\": \"3618.8\"}, {\"time\": \"2:30\", \"load\": \"3827.8\"}, {\"time\": \"3:45\", \"load\": \"4049.8\"}, {\"time\": \"0:00\", \"load\": \"4233.4\"}, {\"time\": \"1:15\", \"load\": \"4390.0\"}, {\"time\": \"2:30\", \"load\": \"4569.0\"}, {\"time\": \"3:45\", \"load\": \"4681.6\"}, {\"time\": \"0:00\", \"load\": \"4811.2\"}, {\"time\": \"1:15\", \"load\": \"4903.8\"}, {\"time\": \"2:30\", \"load\": \"5041.2\"}, {\"time\": \"3:45\", \"load\": \"5209.0\"}, {\"time\": \"0:00\", \"load\": \"5350.4\"}, {\"time\": \"1:15\", \"load\": \"5515.8\"}, {\"time\": \"2:30\", \"load\": \"5703.2\"}, {\"time\": \"3:45\", \"load\": \"5863.8\"}, {\"time\": \"0:00\", \"load\": \"6036.4\"}, {\"time\": \"1:15\", \"load\": \"6234.0\"}, {\"time\": \"2:30\", \"load\": \"6349.4\"}, {\"time\": \"3:45\", \"load\": \"6496.4\"}, {\"time\": \"0:00\", \"load\": \"6561.2\"}, {\"time\": \"1:15\", \"load\": \"6602.4\"}, {\"time\": \"2:30\", \"load\": \"6619.4\"}, {\"time\": \"3:45\", \"load\": \"6628.2\"}]",
    residential_l2_load: "[{\"time\": \"0:00\", \"load\": \"3531.8\"}, {\"time\": \"1:15\", \"load\": \"2741.4\"}, {\"time\": \"2:30\", \"load\": \"2175.0\"}, {\"time\": \"3:45\", \"load\": \"1735.8\"}, {\"time\": \"0:00\", \"load\": \"1398.4\"}, {\"time\": \"1:15\", \"load\": \"1139.2\"}, {\"time\": \"2:30\", \"load\": \"927.8\"}, {\"time\": \"3:45\", \"load\": \"746.6\"}, {\"time\": \"0:00\", \"load\": \"676.6\"}, {\"time\": \"1:15\", \"load\": \"597.4\"}, {\"time\": \"2:30\", \"load\": \"530.6\"}, {\"time\": \"3:45\", \"load\": \"506.6\"}, {\"time\": \"0:00\", \"load\": \"355.0\"}, {\"time\": \"1:15\", \"load\": \"305.6\"}, {\"time\": \"2:30\", \"load\": \"248.8\"}, {\"time\": \"3:45\", \"load\": \"201.6\"}, {\"time\": \"0:00\", \"load\": \"137.6\"}, {\"time\": \"1:15\", \"load\": \"144.2\"}, {\"time\": \"2:30\", \"load\": \"176.0\"}, {\"time\": \"3:45\", \"load\": \"244.2\"}, {\"time\": \"0:00\", \"load\": \"331.8\"}, {\"time\": \"1:15\", \"load\": \"391.6\"}, {\"time\": \"2:30\", \"load\": \"523.6\"}, {\"time\": \"3:45\", \"load\": \"661.2\"}, {\"time\": \"0:00\", \"load\": \"861.4\"}, {\"time\": \"1:15\", \"load\": \"1056.2\"}, {\"time\": \"2:30\", \"load\": \"1399.2\"}, {\"time\": \"3:45\", \"load\": \"1798.2\"}, {\"time\": \"0:00\", \"load\": \"2123.6\"}, {\"time\": \"1:15\", \"load\": \"2490.2\"}, {\"time\": \"2:30\", \"load\": \"2819.0\"}, {\"time\": \"3:45\", \"load\": \"3144.6\"}, {\"time\": \"0:00\", \"load\": \"3527.2\"}, {\"time\": \"1:15\", \"load\": \"3866.4\"}, {\"time\": \"2:30\", \"load\": \"4150.0\"}, {\"time\": \"3:45\", \"load\": \"4353.4\"}, {\"time\": \"0:00\", \"load\": \"4602.0\"}, {\"time\": \"1:15\", \"load\": \"4721.4\"}, {\"time\": \"2:30\", \"load\": \"4862.0\"}, {\"time\": \"3:45\", \"load\": \"4933.6\"}, {\"time\": \"0:00\", \"load\": \"4882.2\"}, {\"time\": \"1:15\", \"load\": \"4966.6\"}, {\"time\": \"2:30\", \"load\": \"4872.0\"}, {\"time\": \"3:45\", \"load\": \"4815.0\"}, {\"time\": \"0:00\", \"load\": \"4712.8\"}, {\"time\": \"1:15\", \"load\": \"4544.2\"}, {\"time\": \"2:30\", \"load\": \"4430.4\"}, {\"time\": \"3:45\", \"load\": \"4181.4\"}, {\"time\": \"0:00\", \"load\": \"3987.6\"}, {\"time\": \"1:15\", \"load\": \"3836.0\"}, {\"time\": \"2:30\", \"load\": \"3791.8\"}, {\"time\": \"3:45\", \"load\": \"3664.2\"}, {\"time\": \"0:00\", \"load\": \"3547.4\"}, {\"time\": \"1:15\", \"load\": \"3320.0\"}, {\"time\": \"2:30\", \"load\": \"3122.0\"}, {\"time\": \"3:45\", \"load\": \"2852.4\"}, {\"time\": \"0:00\", \"load\": \"2726.2\"}, {\"time\": \"1:15\", \"load\": \"2672.8\"}, {\"time\": \"2:30\", \"load\": \"2528.2\"}, {\"time\": \"3:45\", \"load\": \"2320.0\"}, {\"time\": \"0:00\", \"load\": \"2146.8\"}, {\"time\": \"1:15\", \"load\": \"2147.0\"}, {\"time\": \"2:30\", \"load\": \"2057.2\"}, {\"time\": \"3:45\", \"load\": \"2060.2\"}, {\"time\": \"0:00\", \"load\": \"2062.0\"}, {\"time\": \"1:15\", \"load\": \"2188.8\"}, {\"time\": \"2:30\", \"load\": \"2601.6\"}, {\"time\": \"3:45\", \"load\": \"3044.4\"}, {\"time\": \"0:00\", \"load\": \"3611.8\"}, {\"time\": \"1:15\", \"load\": \"4237.8\"}, {\"time\": \"2:30\", \"load\": \"4896.2\"}, {\"time\": \"3:45\", \"load\": \"5577.6\"}, {\"time\": \"0:00\", \"load\": \"6341.0\"}, {\"time\": \"1:15\", \"load\": \"7130.0\"}, {\"time\": \"2:30\", \"load\": \"7785.8\"}, {\"time\": \"3:45\", \"load\": \"8147.6\"}, {\"time\": \"0:00\", \"load\": \"8314.0\"}, {\"time\": \"1:15\", \"load\": \"8621.2\"}, {\"time\": \"2:30\", \"load\": \"8719.2\"}, {\"time\": \"3:45\", \"load\": \"8800.0\"}, {\"time\": \"0:00\", \"load\": \"8637.4\"}, {\"time\": \"1:15\", \"load\": \"8373.8\"}, {\"time\": \"2:30\", \"load\": \"8269.2\"}, {\"time\": \"3:45\", \"load\": \"8232.6\"}, {\"time\": \"0:00\", \"load\": \"7972.4\"}, {\"time\": \"1:15\", \"load\": \"8116.4\"}, {\"time\": \"2:30\", \"load\": \"8231.4\"}, {\"time\": \"3:45\", \"load\": \"8387.2\"}, {\"time\": \"0:00\", \"load\": \"8071.8\"}, {\"time\": \"1:15\", \"load\": \"7824.0\"}, {\"time\": \"2:30\", \"load\": \"7389.8\"}, {\"time\": \"3:45\", \"load\": \"6754.2\"}, {\"time\": \"0:00\", \"load\": \"5969.0\"}, {\"time\": \"1:15\", \"load\": \"5317.8\"}, {\"time\": \"2:30\", \"load\": \"4567.6\"}, {\"time\": \"3:45\", \"load\": \"3861.2\"}]",
    residential_mud_load: "[{\"time\": \"0:00\", \"load\": \"4837.2\"}, {\"time\": \"1:15\", \"load\": \"4027.2\"}, {\"time\": \"2:30\", \"load\": \"3233.2\"}, {\"time\": \"3:45\", \"load\": \"2787.4\"}, {\"time\": \"0:00\", \"load\": \"2261.2\"}, {\"time\": \"1:15\", \"load\": \"1924.2\"}, {\"time\": \"2:30\", \"load\": \"1713.2\"}, {\"time\": \"3:45\", \"load\": \"1533.8\"}, {\"time\": \"0:00\", \"load\": \"1407.4\"}, {\"time\": \"1:15\", \"load\": \"1339.6\"}, {\"time\": \"2:30\", \"load\": \"1239.4\"}, {\"time\": \"3:45\", \"load\": \"1192.0\"}, {\"time\": \"0:00\", \"load\": \"1165.0\"}, {\"time\": \"1:15\", \"load\": \"1141.6\"}, {\"time\": \"2:30\", \"load\": \"1121.4\"}, {\"time\": \"3:45\", \"load\": \"1092.8\"}, {\"time\": \"0:00\", \"load\": \"1078.8\"}, {\"time\": \"1:15\", \"load\": \"1103.4\"}, {\"time\": \"2:30\", \"load\": \"1121.4\"}, {\"time\": \"3:45\", \"load\": \"1161.6\"}, {\"time\": \"0:00\", \"load\": \"1199.8\"}, {\"time\": \"1:15\", \"load\": \"1245.0\"}, {\"time\": \"2:30\", \"load\": \"1280.8\"}, {\"time\": \"3:45\", \"load\": \"1379.4\"}, {\"time\": \"0:00\", \"load\": \"1522.6\"}, {\"time\": \"1:15\", \"load\": \"1645.2\"}, {\"time\": \"2:30\", \"load\": \"1842.8\"}, {\"time\": \"3:45\", \"load\": \"2110.6\"}, {\"time\": \"0:00\", \"load\": \"2318.4\"}, {\"time\": \"1:15\", \"load\": \"2563.4\"}, {\"time\": \"2:30\", \"load\": \"2855.4\"}, {\"time\": \"3:45\", \"load\": \"3138.6\"}, {\"time\": \"0:00\", \"load\": \"3443.8\"}, {\"time\": \"1:15\", \"load\": \"3779.8\"}, {\"time\": \"2:30\", \"load\": \"4019.2\"}, {\"time\": \"3:45\", \"load\": \"4379.6\"}, {\"time\": \"0:00\", \"load\": \"4588.4\"}, {\"time\": \"1:15\", \"load\": \"4784.4\"}, {\"time\": \"2:30\", \"load\": \"4917.0\"}, {\"time\": \"3:45\", \"load\": \"4969.4\"}, {\"time\": \"0:00\", \"load\": \"5030.8\"}, {\"time\": \"1:15\", \"load\": \"5086.0\"}, {\"time\": \"2:30\", \"load\": \"5014.4\"}, {\"time\": \"3:45\", \"load\": \"4946.6\"}, {\"time\": \"0:00\", \"load\": \"4720.8\"}, {\"time\": \"1:15\", \"load\": \"4619.4\"}, {\"time\": \"2:30\", \"load\": \"4546.8\"}, {\"time\": \"3:45\", \"load\": \"4554.8\"}, {\"time\": \"0:00\", \"load\": \"4529.4\"}, {\"time\": \"1:15\", \"load\": \"4551.0\"}, {\"time\": \"2:30\", \"load\": \"4567.4\"}, {\"time\": \"3:45\", \"load\": \"4757.4\"}, {\"time\": \"0:00\", \"load\": \"4914.0\"}, {\"time\": \"1:15\", \"load\": \"5212.8\"}, {\"time\": \"2:30\", \"load\": \"5448.2\"}, {\"time\": \"3:45\", \"load\": \"5636.8\"}, {\"time\": \"0:00\", \"load\": \"5957.6\"}, {\"time\": \"1:15\", \"load\": \"6258.8\"}, {\"time\": \"2:30\", \"load\": \"6529.0\"}, {\"time\": \"3:45\", \"load\": \"6847.0\"}, {\"time\": \"0:00\", \"load\": \"7255.8\"}, {\"time\": \"1:15\", \"load\": \"7607.4\"}, {\"time\": \"2:30\", \"load\": \"7842.0\"}, {\"time\": \"3:45\", \"load\": \"8150.6\"}, {\"time\": \"0:00\", \"load\": \"8535.4\"}, {\"time\": \"1:15\", \"load\": \"8935.0\"}, {\"time\": \"2:30\", \"load\": \"9410.6\"}, {\"time\": \"3:45\", \"load\": \"9955.0\"}, {\"time\": \"0:00\", \"load\": \"10630.6\"}, {\"time\": \"1:15\", \"load\": \"11410.6\"}, {\"time\": \"2:30\", \"load\": \"12327.6\"}, {\"time\": \"3:45\", \"load\": \"13285.4\"}, {\"time\": \"0:00\", \"load\": \"14138.0\"}, {\"time\": \"1:15\", \"load\": \"14843.6\"}, {\"time\": \"2:30\", \"load\": \"15487.2\"}, {\"time\": \"3:45\", \"load\": \"15574.2\"}, {\"time\": \"0:00\", \"load\": \"15589.0\"}, {\"time\": \"1:15\", \"load\": \"14859.4\"}, {\"time\": \"2:30\", \"load\": \"14667.2\"}, {\"time\": \"3:45\", \"load\": \"14051.6\"}, {\"time\": \"0:00\", \"load\": \"13526.2\"}, {\"time\": \"1:15\", \"load\": \"13061.0\"}, {\"time\": \"2:30\", \"load\": \"12990.0\"}, {\"time\": \"3:45\", \"load\": \"13104.2\"}, {\"time\": \"0:00\", \"load\": \"13136.0\"}, {\"time\": \"1:15\", \"load\": \"12928.4\"}, {\"time\": \"2:30\", \"load\": \"13080.6\"}, {\"time\": \"3:45\", \"load\": \"13167.0\"}, {\"time\": \"0:00\", \"load\": \"12951.6\"}, {\"time\": \"1:15\", \"load\": \"12250.4\"}, {\"time\": \"2:30\", \"load\": \"11292.6\"}, {\"time\": \"3:45\", \"load\": \"10133.6\"}, {\"time\": \"0:00\", \"load\": \"8997.6\"}, {\"time\": \"1:15\", \"load\": \"8069.0\"}, {\"time\": \"2:30\", \"load\": \"7062.0\"}, {\"time\": \"3:45\", \"load\": \"5831.2\"}]",
    work_load: "[{\"time\": \"0:00\", \"load\": \"214.0\"}, {\"time\": \"1:15\", \"load\": \"136.6\"}, {\"time\": \"2:30\", \"load\": \"92.2\"}, {\"time\": \"3:45\", \"load\": \"68.4\"}, {\"time\": \"0:00\", \"load\": \"39.6\"}, {\"time\": \"1:15\", \"load\": \"22.4\"}, {\"time\": \"2:30\", \"load\": \"13.2\"}, {\"time\": \"3:45\", \"load\": \"13.2\"}, {\"time\": \"0:00\", \"load\": \"13.2\"}, {\"time\": \"1:15\", \"load\": \"13.2\"}, {\"time\": \"2:30\", \"load\": \"12.6\"}, {\"time\": \"3:45\", \"load\": \"6.6\"}, {\"time\": \"0:00\", \"load\": \"13.2\"}, {\"time\": \"1:15\", \"load\": \"13.2\"}, {\"time\": \"2:30\", \"load\": \"13.2\"}, {\"time\": \"3:45\", \"load\": \"13.2\"}, {\"time\": \"0:00\", \"load\": \"26.4\"}, {\"time\": \"1:15\", \"load\": \"33.8\"}, {\"time\": \"2:30\", \"load\": \"63.4\"}, {\"time\": \"3:45\", \"load\": \"105.6\"}, {\"time\": \"0:00\", \"load\": \"151.2\"}, {\"time\": \"1:15\", \"load\": \"225.8\"}, {\"time\": \"2:30\", \"load\": \"368.6\"}, {\"time\": \"3:45\", \"load\": \"588.4\"}, {\"time\": \"0:00\", \"load\": \"859.2\"}, {\"time\": \"1:15\", \"load\": \"1293.4\"}, {\"time\": \"2:30\", \"load\": \"1691.6\"}, {\"time\": \"3:45\", \"load\": \"2179.4\"}, {\"time\": \"0:00\", \"load\": \"2755.0\"}, {\"time\": \"1:15\", \"load\": \"3753.4\"}, {\"time\": \"2:30\", \"load\": \"4979.4\"}, {\"time\": \"3:45\", \"load\": \"6319.8\"}, {\"time\": \"0:00\", \"load\": \"8056.8\"}, {\"time\": \"1:15\", \"load\": \"9930.6\"}, {\"time\": \"2:30\", \"load\": \"11823.6\"}, {\"time\": \"3:45\", \"load\": \"13611.8\"}, {\"time\": \"0:00\", \"load\": \"15132.2\"}, {\"time\": \"1:15\", \"load\": \"16132.2\"}, {\"time\": \"2:30\", \"load\": \"16236.4\"}, {\"time\": \"3:45\", \"load\": \"15498.4\"}, {\"time\": \"0:00\", \"load\": \"14495.0\"}, {\"time\": \"1:15\", \"load\": \"13152.8\"}, {\"time\": \"2:30\", \"load\": \"11508.4\"}, {\"time\": \"3:45\", \"load\": \"9888.0\"}, {\"time\": \"0:00\", \"load\": \"8763.4\"}, {\"time\": \"1:15\", \"load\": \"7760.4\"}, {\"time\": \"2:30\", \"load\": \"6817.0\"}, {\"time\": \"3:45\", \"load\": \"6169.2\"}, {\"time\": \"0:00\", \"load\": \"5682.2\"}, {\"time\": \"1:15\", \"load\": \"5378.2\"}, {\"time\": \"2:30\", \"load\": \"4895.6\"}, {\"time\": \"3:45\", \"load\": \"4589.0\"}, {\"time\": \"0:00\", \"load\": \"4433.6\"}, {\"time\": \"1:15\", \"load\": \"4183.4\"}, {\"time\": \"2:30\", \"load\": \"3862.2\"}, {\"time\": \"3:45\", \"load\": \"3508.2\"}, {\"time\": \"0:00\", \"load\": \"3271.4\"}, {\"time\": \"1:15\", \"load\": \"3050.0\"}, {\"time\": \"2:30\", \"load\": \"2972.2\"}, {\"time\": \"3:45\", \"load\": \"3014.2\"}, {\"time\": \"0:00\", \"load\": \"3046.6\"}, {\"time\": \"1:15\", \"load\": \"3252.4\"}, {\"time\": \"2:30\", \"load\": \"3322.6\"}, {\"time\": \"3:45\", \"load\": \"3420.4\"}, {\"time\": \"0:00\", \"load\": \"3617.0\"}, {\"time\": \"1:15\", \"load\": \"3646.6\"}, {\"time\": \"2:30\", \"load\": \"3651.0\"}, {\"time\": \"3:45\", \"load\": \"3594.4\"}, {\"time\": \"0:00\", \"load\": \"3546.4\"}, {\"time\": \"1:15\", \"load\": \"3397.0\"}, {\"time\": \"2:30\", \"load\": \"3222.8\"}, {\"time\": \"3:45\", \"load\": \"3085.8\"}, {\"time\": \"0:00\", \"load\": \"2900.2\"}, {\"time\": \"1:15\", \"load\": \"2884.4\"}, {\"time\": \"2:30\", \"load\": \"2742.6\"}, {\"time\": \"3:45\", \"load\": \"2660.2\"}, {\"time\": \"0:00\", \"load\": \"2593.8\"}, {\"time\": \"1:15\", \"load\": \"2518.0\"}, {\"time\": \"2:30\", \"load\": \"2403.0\"}, {\"time\": \"3:45\", \"load\": \"2333.2\"}, {\"time\": \"0:00\", \"load\": \"2200.8\"}, {\"time\": \"1:15\", \"load\": \"2079.6\"}, {\"time\": \"2:30\", \"load\": \"1952.0\"}, {\"time\": \"3:45\", \"load\": \"1750.0\"}, {\"time\": \"0:00\", \"load\": \"1539.8\"}, {\"time\": \"1:15\", \"load\": \"1405.2\"}, {\"time\": \"2:30\", \"load\": \"1238.4\"}, {\"time\": \"3:45\", \"load\": \"1105.6\"}, {\"time\": \"0:00\", \"load\": \"939.4\"}, {\"time\": \"1:15\", \"load\": \"820.8\"}, {\"time\": \"2:30\", \"load\": \"707.6\"}, {\"time\": \"3:45\", \"load\": \"583.6\"}, {\"time\": \"0:00\", \"load\": \"469.6\"}, {\"time\": \"1:15\", \"load\": \"383.8\"}, {\"time\": \"2:30\", \"load\": \"289.8\"}, {\"time\": \"3:45\", \"load\": \"250.8\"}]",
    fast_load: "[{\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"350.0\"}, {\"time\": \"3:45\", \"load\": \"70.0\"}, {\"time\": \"0:00\", \"load\": \"350.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"70.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"350.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"70.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"350.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"700.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"700.0\"}, {\"time\": \"0:00\", \"load\": \"350.0\"}, {\"time\": \"1:15\", \"load\": \"650.0\"}, {\"time\": \"2:30\", \"load\": \"700.0\"}, {\"time\": \"3:45\", \"load\": \"350.0\"}, {\"time\": \"0:00\", \"load\": \"910.0\"}, {\"time\": \"1:15\", \"load\": \"1300.0\"}, {\"time\": \"2:30\", \"load\": \"1400.0\"}, {\"time\": \"3:45\", \"load\": \"2610.0\"}, {\"time\": \"0:00\", \"load\": \"1790.0\"}, {\"time\": \"1:15\", \"load\": \"2040.0\"}, {\"time\": \"2:30\", \"load\": \"1050.0\"}, {\"time\": \"3:45\", \"load\": \"2660.0\"}, {\"time\": \"0:00\", \"load\": \"3800.0\"}, {\"time\": \"1:15\", \"load\": \"1530.0\"}, {\"time\": \"2:30\", \"load\": \"910.0\"}, {\"time\": \"3:45\", \"load\": \"2790.0\"}, {\"time\": \"0:00\", \"load\": \"2820.0\"}, {\"time\": \"1:15\", \"load\": \"1510.0\"}, {\"time\": \"2:30\", \"load\": \"2500.0\"}, {\"time\": \"3:45\", \"load\": \"3530.0\"}, {\"time\": \"0:00\", \"load\": \"3640.0\"}, {\"time\": \"1:15\", \"load\": \"1510.0\"}, {\"time\": \"2:30\", \"load\": \"1400.0\"}, {\"time\": \"3:45\", \"load\": \"2290.0\"}, {\"time\": \"0:00\", \"load\": \"1570.0\"}, {\"time\": \"1:15\", \"load\": \"2750.0\"}, {\"time\": \"2:30\", \"load\": \"1550.0\"}, {\"time\": \"3:45\", \"load\": \"3850.0\"}, {\"time\": \"0:00\", \"load\": \"1650.0\"}, {\"time\": \"1:15\", \"load\": \"2340.0\"}, {\"time\": \"2:30\", \"load\": \"1490.0\"}, {\"time\": \"3:45\", \"load\": \"1750.0\"}, {\"time\": \"0:00\", \"load\": \"1030.0\"}, {\"time\": \"1:15\", \"load\": \"2970.0\"}, {\"time\": \"2:30\", \"load\": \"1550.0\"}, {\"time\": \"3:45\", \"load\": \"1430.0\"}, {\"time\": \"0:00\", \"load\": \"810.0\"}, {\"time\": \"1:15\", \"load\": \"1960.0\"}, {\"time\": \"2:30\", \"load\": \"1780.0\"}, {\"time\": \"3:45\", \"load\": \"1060.0\"}, {\"time\": \"0:00\", \"load\": \"1150.0\"}, {\"time\": \"1:15\", \"load\": \"640.0\"}, {\"time\": \"2:30\", \"load\": \"950.0\"}, {\"time\": \"3:45\", \"load\": \"1150.0\"}, {\"time\": \"0:00\", \"load\": \"1050.0\"}, {\"time\": \"1:15\", \"load\": \"2260.0\"}, {\"time\": \"2:30\", \"load\": \"2130.0\"}, {\"time\": \"3:45\", \"load\": \"660.0\"}, {\"time\": \"0:00\", \"load\": \"770.0\"}, {\"time\": \"1:15\", \"load\": \"200.0\"}, {\"time\": \"2:30\", \"load\": \"300.0\"}, {\"time\": \"3:45\", \"load\": \"1070.0\"}, {\"time\": \"0:00\", \"load\": \"700.0\"}, {\"time\": \"1:15\", \"load\": \"1140.0\"}, {\"time\": \"2:30\", \"load\": \"700.0\"}, {\"time\": \"3:45\", \"load\": \"610.0\"}, {\"time\": \"0:00\", \"load\": \"710.0\"}, {\"time\": \"1:15\", \"load\": \"1000.0\"}, {\"time\": \"2:30\", \"load\": \"980.0\"}, {\"time\": \"3:45\", \"load\": \"550.0\"}, {\"time\": \"0:00\", \"load\": \"240.0\"}, {\"time\": \"1:15\", \"load\": \"720.0\"}, {\"time\": \"2:30\", \"load\": \"20.0\"}, {\"time\": \"3:45\", \"load\": \"530.0\"}, {\"time\": \"0:00\", \"load\": \"350.0\"}, {\"time\": \"1:15\", \"load\": \"350.0\"}, {\"time\": \"2:30\", \"load\": \"350.0\"}, {\"time\": \"3:45\", \"load\": \"590.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"190.0\"}, {\"time\": \"2:30\", \"load\": \"700.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}]",
    public_l2_load: "[{\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}, {\"time\": \"0:00\", \"load\": \"0.0\"}, {\"time\": \"1:15\", \"load\": \"0.0\"}, {\"time\": \"2:30\", \"load\": \"0.0\"}, {\"time\": \"3:45\", \"load\": \"0.0\"}]",
    total_load: "[{\"time\": \"0:00\", \"load\": \"15217.6\"}, {\"time\": \"1:15\", \"load\": \"13504.0\"}, {\"time\": \"2:30\", \"load\": \"12426.8\"}, {\"time\": \"3:45\", \"load\": \"11221.0\"}, {\"time\": \"0:00\", \"load\": \"10535.2\"}, {\"time\": \"1:15\", \"load\": \"9506.4\"}, {\"time\": \"2:30\", \"load\": \"8980.4\"}, {\"time\": \"3:45\", \"load\": \"8527.4\"}, {\"time\": \"0:00\", \"load\": \"8200.0\"}, {\"time\": \"1:15\", \"load\": \"7979.2\"}, {\"time\": \"2:30\", \"load\": \"7577.2\"}, {\"time\": \"3:45\", \"load\": \"7655.2\"}, {\"time\": \"0:00\", \"load\": \"6912.0\"}, {\"time\": \"1:15\", \"load\": \"6604.6\"}, {\"time\": \"2:30\", \"load\": \"6259.6\"}, {\"time\": \"3:45\", \"load\": \"5927.8\"}, {\"time\": \"0:00\", \"load\": \"5590.6\"}, {\"time\": \"1:15\", \"load\": \"5431.4\"}, {\"time\": \"2:30\", \"load\": \"5145.6\"}, {\"time\": \"3:45\", \"load\": \"5339.4\"}, {\"time\": \"0:00\", \"load\": \"4891.4\"}, {\"time\": \"1:15\", \"load\": \"5515.6\"}, {\"time\": \"2:30\", \"load\": \"4914.8\"}, {\"time\": \"3:45\", \"load\": \"5904.6\"}, {\"time\": \"0:00\", \"load\": \"5976.4\"}, {\"time\": \"1:15\", \"load\": \"6869.4\"}, {\"time\": \"2:30\", \"load\": \"7721.8\"}, {\"time\": \"3:45\", \"load\": \"8393.6\"}, {\"time\": \"0:00\", \"load\": \"9974.4\"}, {\"time\": \"1:15\", \"load\": \"11921.4\"}, {\"time\": \"2:30\", \"load\": \"13824.4\"}, {\"time\": \"3:45\", \"load\": \"16967.4\"}, {\"time\": \"0:00\", \"load\": \"18573.6\"}, {\"time\": \"1:15\", \"load\": \"21377.4\"}, {\"time\": \"2:30\", \"load\": \"22817.0\"}, {\"time\": \"3:45\", \"load\": \"26790.2\"}, {\"time\": \"0:00\", \"load\": \"29938.6\"}, {\"time\": \"1:15\", \"load\": \"29018.4\"}, {\"time\": \"2:30\", \"load\": \"28826.4\"}, {\"time\": \"3:45\", \"load\": \"30144.8\"}, {\"time\": \"0:00\", \"load\": \"29226.4\"}, {\"time\": \"1:15\", \"load\": \"26767.4\"}, {\"time\": \"2:30\", \"load\": \"25971.6\"}, {\"time\": \"3:45\", \"load\": \"25280.6\"}, {\"time\": \"0:00\", \"load\": \"23975.4\"}, {\"time\": \"1:15\", \"load\": \"20592.4\"}, {\"time\": \"2:30\", \"load\": \"19386.0\"}, {\"time\": \"3:45\", \"load\": \"19411.2\"}, {\"time\": \"0:00\", \"load\": \"18018.2\"}, {\"time\": \"1:15\", \"load\": \"18781.0\"}, {\"time\": \"2:30\", \"load\": \"17108.0\"}, {\"time\": \"3:45\", \"load\": \"19177.2\"}, {\"time\": \"0:00\", \"load\": \"16883.4\"}, {\"time\": \"1:15\", \"load\": \"17414.4\"}, {\"time\": \"2:30\", \"load\": \"16311.2\"}, {\"time\": \"3:45\", \"load\": \"16166.4\"}, {\"time\": \"0:00\", \"load\": \"15422.8\"}, {\"time\": \"1:15\", \"load\": \"17407.6\"}, {\"time\": \"2:30\", \"load\": \"16049.4\"}, {\"time\": \"3:45\", \"load\": \"16099.6\"}, {\"time\": \"0:00\", \"load\": \"15778.6\"}, {\"time\": \"1:15\", \"load\": \"17496.2\"}, {\"time\": \"2:30\", \"load\": \"17555.2\"}, {\"time\": \"3:45\", \"load\": \"17262.8\"}, {\"time\": \"0:00\", \"load\": \"17935.0\"}, {\"time\": \"1:15\", \"load\": \"18009.2\"}, {\"time\": \"2:30\", \"load\": \"19236.0\"}, {\"time\": \"3:45\", \"load\": \"20417.6\"}, {\"time\": \"0:00\", \"load\": \"21577.4\"}, {\"time\": \"1:15\", \"load\": \"24138.4\"}, {\"time\": \"2:30\", \"load\": \"25587.0\"}, {\"time\": \"3:45\", \"load\": \"25796.0\"}, {\"time\": \"0:00\", \"load\": \"27556.0\"}, {\"time\": \"1:15\", \"load\": \"28676.8\"}, {\"time\": \"2:30\", \"load\": \"30143.4\"}, {\"time\": \"3:45\", \"load\": \"31501.8\"}, {\"time\": \"0:00\", \"load\": \"31430.2\"}, {\"time\": \"1:15\", \"load\": \"31528.6\"}, {\"time\": \"2:30\", \"load\": \"31058.4\"}, {\"time\": \"3:45\", \"load\": \"30476.4\"}, {\"time\": \"0:00\", \"load\": \"29885.6\"}, {\"time\": \"1:15\", \"load\": \"29418.2\"}, {\"time\": \"2:30\", \"load\": \"29232.4\"}, {\"time\": \"3:45\", \"load\": \"28845.8\"}, {\"time\": \"0:00\", \"load\": \"28238.6\"}, {\"time\": \"1:15\", \"load\": \"28685.8\"}, {\"time\": \"2:30\", \"load\": \"28273.6\"}, {\"time\": \"3:45\", \"load\": \"29053.6\"}, {\"time\": \"0:00\", \"load\": \"28349.2\"}, {\"time\": \"1:15\", \"load\": \"27479.2\"}, {\"time\": \"2:30\", \"load\": \"26089.4\"}, {\"time\": \"3:45\", \"load\": \"24557.8\"}, {\"time\": \"0:00\", \"load\": \"21997.4\"}, {\"time\": \"1:15\", \"load\": \"20563.0\"}, {\"time\": \"2:30\", \"load\": \"19238.8\"}, {\"time\": \"3:45\", \"load\": \"16571.4\"}]"
}];
