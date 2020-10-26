export const loadControlDefaultParams = {
    county: "Santa Clara",
    rate_energy_peak: 0.16997,
    rate_energy_partpeak: 0.12236,
    rate_energy_offpeak: 0.09082,
    rate_demand_peak: 21.23,
    rate_demand_partpeak: 5.85,
    rate_demand_overall: 19.10,
};

export const loadForecastDefaultParams = {

    config_name: "",
    aggregation_level: "county",
    num_evs: 100000,
    county_choice: "Santa Clara",
    fast_percent: 0.1,
    work_percent: 0.2,
    res_percent: 0.7,
    l1_percent: 0.5,
    public_l2_percent: 0.0,

    res_daily_use: 1.0,
    work_daily_use: 1.0,
    fast_daily_use: 0.5,
    rent_percent: 0.4,

    res_l2_smooth: true,
    week_day: true,
    publicl2_daily_use: 0.33,
    small_batt: 0,
    big_batt: 0.7,
    all_batt: 0.3,
    timer_control: "None",
    work_control: "minpeak",
};
