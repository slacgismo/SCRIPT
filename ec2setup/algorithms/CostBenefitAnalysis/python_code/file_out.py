from __future__ import division
from __future__ import unicode_literals

from past.utils import old_div
from builtins import range
import csv
import helpers

def export_results(model_instance):

    # Utility Revenue
    annual_bills = [model_instance.total_revenue[year] for year in model_instance.model_years]
    annual_energy_bills = [model_instance.volumetric_revenue[year] for year in model_instance.model_years]
    annual_demand_bills = [model_instance.demand_revenue[year] for year in model_instance.model_years]
    npv_bills = helpers.npv(annual_bills, model_instance.inputs.discount_rate)[0]
    npv_volumetric = helpers.npv(annual_energy_bills, model_instance.inputs.discount_rate)[0]
    npv_demand = helpers.npv(annual_demand_bills, model_instance.inputs.discount_rate)[0]

    annual_resbills = [model_instance.res_revenue[year] for year in model_instance.model_years]
    npv_resbills = helpers.npv(annual_resbills, model_instance.inputs.discount_rate)[0]

    annual_workbills = [model_instance.work_revenue[year] for year in model_instance.model_years]
    npv_workbills = helpers.npv(annual_workbills, model_instance.inputs.discount_rate)[0]

    annual_publicl2bills = [model_instance.publicl2_revenue[year] for year in model_instance.model_years]
    npv_publicl2bills = helpers.npv(annual_publicl2bills, model_instance.inputs.discount_rate)[0]

    annual_dcfcbills = [model_instance.dcfc_revenue[year] for year in model_instance.model_years]
    npv_dcfcbills = helpers.npv(annual_dcfcbills, model_instance.inputs.discount_rate)[0]


    # Vehicle costs
    annual_vehcosts = [model_instance.vehicles.capital_cost[year] for year in model_instance.model_years]
    npv_vehcosts = helpers.npv(annual_vehcosts, model_instance.inputs.discount_rate)[0]


    # Charger costs
    annual_chgcosts = [model_instance.chargers.res_cost[year]
                           + model_instance.chargers.workplace_l2_cost[year]
                           + model_instance.chargers.public_l2_cost[year]
                           + model_instance.chargers.dcfc_cost[year] for year in model_instance.model_years]
    npv_chgcosts = helpers.npv(annual_chgcosts, model_instance.inputs.discount_rate)[0]

    annual_reschgcosts = [model_instance.chargers.res_cost[year] for year in model_instance.model_years]
    npv_reschgcosts = helpers.npv(annual_reschgcosts, model_instance.inputs.discount_rate)[0]

    annual_workl2chgcosts = [model_instance.chargers.workplace_l2_cost[year] for year in model_instance.model_years]
    npv_workl2chgcosts = helpers.npv(annual_workl2chgcosts, model_instance.inputs.discount_rate)[0]

    annual_publicl2chgcosts = [model_instance.chargers.public_l2_cost[year] for year in model_instance.model_years]
    npv_publicl2chgcosts = helpers.npv(annual_publicl2chgcosts, model_instance.inputs.discount_rate)[0]

    annual_dcfcchgcosts = [model_instance.chargers.dcfc_cost[year] for year in model_instance.model_years]
    npv_dcfcchgcosts = helpers.npv(annual_dcfcchgcosts, model_instance.inputs.discount_rate)[0]


    # Gasoline savings
    annual_gassavings = [model_instance.vehicles.gasoline_savings[year] for year in model_instance.model_years]
    annual_gallons_avoided = [model_instance.vehicles.gallons_avoided[year] for year in model_instance.model_years]
    npv_gassavings = helpers.npv(annual_gassavings, model_instance.inputs.discount_rate)[0]

    # Gasoline consumption
    annual_gas_consumption = [model_instance.vehicles.gasoline_consumption[year] for year in
                              model_instance.vehicles.gas_consumption_range]

    annual_gas_consumption_mmbtu = [model_instance.vehicles.gasoline_consumption_mmbtu[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    annual_gas_consumption_co2 = [model_instance.vehicles.gasoline_consumption_co2[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev10_annual_gas_consumption = [model_instance.vehicles.phev10_gasoline_consumption[year] for year in
                              model_instance.vehicles.gas_consumption_range]

    phev10_annual_gas_consumption_mmbtu = [model_instance.vehicles.phev10_gasoline_consumption_mmbtu[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev10_annual_gas_consumption_co2 = [model_instance.vehicles.phev10_gasoline_consumption_co2[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev20_annual_gas_consumption = [model_instance.vehicles.phev20_gasoline_consumption[year] for year in
                              model_instance.vehicles.gas_consumption_range]

    phev20_annual_gas_consumption_mmbtu = [model_instance.vehicles.phev20_gasoline_consumption_mmbtu[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev20_annual_gas_consumption_co2 = [model_instance.vehicles.phev20_gasoline_consumption_co2[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev40_annual_gas_consumption = [model_instance.vehicles.phev40_gasoline_consumption[year] for year in
                              model_instance.vehicles.gas_consumption_range]

    phev40_annual_gas_consumption_mmbtu = [model_instance.vehicles.phev40_gasoline_consumption_mmbtu[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    phev40_annual_gas_consumption_co2 = [model_instance.vehicles.phev40_gasoline_consumption_co2[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    bev100_annual_gas_consumption = [model_instance.vehicles.bev100_gasoline_consumption[year] for year in
                              model_instance.vehicles.gas_consumption_range]

    bev100_annual_gas_consumption_mmbtu = [model_instance.vehicles.bev100_gasoline_consumption_mmbtu[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    bev100_annual_gas_consumption_co2 = [model_instance.vehicles.bev100_gasoline_consumption_co2[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    ev_share = [model_instance.vehicles.ev_share[year] for year in
                                    model_instance.vehicles.gas_consumption_range]

    npv_gas_consumption = helpers.npv(annual_gas_consumption, model_instance.inputs.discount_rate)[0]

    # Avoided O&M
    annual_oandm = [model_instance.vehicles.oandm_savings[year] for year in model_instance.model_years]
    npv_oandm = helpers.npv(annual_oandm, model_instance.inputs.discount_rate)[0]


    # Tax credt
    annual_taxcredit = [model_instance.vehicles.tax_credit[year] for year in model_instance.model_years]
    npv_taxcredit = helpers.npv(annual_taxcredit, model_instance.inputs.discount_rate)[0]

    # Vehicle sales
    annual_sales = [model_instance.vehicles.sales[year] for year in model_instance.model_years]
    npv_sales = helpers.npv(annual_sales, model_instance.inputs.discount_rate)[0]

    # Cumulative vehicle population
    cumulative_ev_population = [model_instance.vehicles.population[year] for year in model_instance.model_years]
    cumulative_ldv_population = [model_instance.vehicles.total_population[year] for year in model_instance.model_years]
    ev_sales_proportion = [old_div(model_instance.vehicles.sales[year],model_instance.vehicles.total_population[year])
                           for year in range(model_instance.inputs.start_year, model_instance.inputs.end_year)]
    # Peak Demand 5 - 9 PM

    peak_demand_5to9_pm = [model_instance.peak_demand_5to9_pm[year] for year in model_instance.model_years]

    annual_tandd = []
    for year in model_instance.model_years:
        try:
            annual_tandd.append(model_instance.t_and_d_dict[year])
        except KeyError:
            annual_tandd.append(0)
    npv_tandd = helpers.npv(annual_tandd, model_instance.inputs.discount_rate)[0]

    annual_distribution = []
    for year in model_instance.model_years:
        try:
            annual_distribution.append(model_instance.distribution_dict[year])
        except KeyError:
            annual_tandd.append(0)
    npv_distribution = helpers.npv(annual_distribution, model_instance.inputs.discount_rate)[0]

    annual_transmission = []
    for year in model_instance.model_years:
        try:
            annual_transmission.append(model_instance.transmission_dict[year])
        except KeyError:
            annual_tandd.append(0)
    npv_transmission = helpers.npv(annual_transmission, model_instance.inputs.discount_rate)[0]

    # Energy Supply cost
    annual_energy_supply_cost = []
    for year in model_instance.model_years:
        try:
            annual_energy_supply_cost.append(model_instance.annual_energy_supply_cost_dict[year])
        except KeyError:
            annual_energy_supply_cost.append(0)

    npv_energy = helpers.npv(annual_energy_supply_cost, model_instance.inputs.discount_rate)[0]

    annual_energy = []
    for year in model_instance.model_years:
        try:
            annual_energy .append(model_instance.energy_dict[year])
        except KeyError:
            annual_tandd.append(0)
    npv_energy = helpers.npv(annual_energy, model_instance.inputs.discount_rate)[0]

    annual_capacity = []
    for year in model_instance.model_years:
        try:
            annual_capacity.append(model_instance.capacity_dict[year])
        except KeyError:
            annual_tandd.append(0)
    npv_capacity = helpers.npv(annual_capacity, model_instance.inputs.discount_rate)[0]

    # SRP Emissions
    CO2_emissions = []
    NOX_emissions = []
    PM10_emissions = []
    SO2_emissions = []
    VOC_emissions = []

    for year in model_instance.model_years:
        try:
            CO2_emissions.append(model_instance.CO2_emissions_dict[year])
            NOX_emissions.append(model_instance.NOX_emissions_dict[year])
            PM10_emissions.append(model_instance.PM10_emissions_dict[year])
            SO2_emissions.append(model_instance.SO2_emissions_dict[year])
            VOC_emissions.append(model_instance.VOC_emissions_dict[year])
        except KeyError:
            CO2_emissions.append(0)
            NOX_emissions.append(0)
            PM10_emissions.append(0)
            SO2_emissions.append(0)
            VOC_emissions.append(0)

    npv_results_dir = model_instance.inputs.RESULTS_DIR + r'\npv_results.csv'
    with open(npv_results_dir, 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(['Year', 'NPV'])

        # Bill revenue
        writer.writerow(['Utility Bills', npv_bills])
        writer.writerow(['Utility Bills (volumetric)', npv_volumetric])
        writer.writerow(['Utility Bills (demand)', npv_demand])
        writer.writerow(['Utility Bills (res)', npv_resbills])
        writer.writerow(['Utility Bills (work)', npv_workbills])
        writer.writerow(['Utility Bills (pub L2)', npv_publicl2bills])
        writer.writerow(['Utility Bills (DCFC)', npv_dcfcbills])

        # Incremental capital cost
        writer.writerow(['Incremental upfront vehicle cost', npv_vehcosts])

        # Charger cost
        writer.writerow(['Charging infrastructure cost', npv_chgcosts])
        writer.writerow(['Charging infrastructure cost (res)', npv_reschgcosts])
        writer.writerow(['Charging infrastructure cost (work L2)', npv_workl2chgcosts])
        writer.writerow(['Charging infrastructure cost (public L2)', npv_publicl2chgcosts])
        writer.writerow(['Charging infrastructure cost (DCFC)', npv_dcfcchgcosts])

        # Avoided gasoline cost
        writer.writerow(['Avoided vehicle gasoline', npv_gassavings])

        # Avoided O&M cost
        writer.writerow(['Vehicle O&M Savings', npv_oandm])

        # Tax credit
        writer.writerow(['Federal EV Tax Credit', npv_taxcredit])

        # Energy Supply Cost

        writer.writerow(['Energy Supply Cost', npv_energy])
        writer.writerow(['Energy Cost', npv_energy])
        writer.writerow(['Generation Capacity Cost', npv_capacity])

        # Vehicle Sales
        writer.writerow(['Vehicle Sales (NPV)', npv_sales])

        # Distribution cost
        writer.writerow(['Transmission and Distribution Cost', npv_tandd])
        writer.writerow(['Distribution Cost', npv_distribution])
        writer.writerow(['Transmission Cost', npv_transmission])

    annual_results_dir = model_instance.inputs.RESULTS_DIR + r'\annual_results.csv'
    with open(annual_results_dir, 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(['Year']
                        + model_instance.model_years)

        # Bill revenue
        writer.writerow(['Utility Bills']
                        + annual_bills)
        writer.writerow(['Utility Bills (res)']
                        + annual_resbills)
        writer.writerow(['Utility Bills (work)']
                        + annual_workbills)
        writer.writerow(['Utility Bills (pub L2)']
                            + annual_publicl2bills)
        writer.writerow(['Utility Bills (DCFC)']
                        + annual_dcfcbills)

        # Incremental capital cost
        writer.writerow(['Incremental upfront vehicle cost']
                        + annual_vehcosts)

        # Charger cost
        writer.writerow(['Charging infrastructure cost']
                        + annual_chgcosts)
        writer.writerow(['Charging infrastructure cost (res)']
                        + annual_reschgcosts)
        writer.writerow(['Charging infrastructure cost (work L2)']
                        + annual_workl2chgcosts)
        writer.writerow(['Charging infrastructure cost (public L2)']
                        + annual_publicl2chgcosts)
        writer.writerow(['Charging infrastructure cost (DCFC)']
                        + annual_dcfcchgcosts)

        # Avoided gasoline cost
        writer.writerow(['Avoided vehicle gasoline ($)']
                        + annual_gassavings)

        writer.writerow(['Avoided vehicle gasoline (gallons)']
                        + annual_gallons_avoided)

        # Avoided O&M cost
        writer.writerow(['Vehicle O&M Savings']
                        + annual_oandm)

        # Tax credit
        writer.writerow(['Federal EV Tax Credit']
                        + annual_taxcredit)

        # Vehicle sales
        writer.writerow(['Vehicle sales']
                        + annual_sales)

        # Distribution cost
        writer.writerow(['Transmission and Distribution Cost']
                        + annual_tandd)
        writer.writerow(['Distribution Cost']
                        + annual_distribution)
        writer.writerow(['Transmission Cost']
                        + annual_transmission)

        # Populations

        writer.writerow(['Cumulative personal light-duty EV population'] + cumulative_ev_population)
        writer.writerow(['Cumulative personal light-duty LDV population'] + cumulative_ldv_population)
        writer.writerow(['EV sales as % of total personal light-duty vehicles'] + ev_sales_proportion)

        # Annual results
        writer.writerow(['Peak Demand 5-9 PM'] + peak_demand_5to9_pm)

        # Energy supply cost
        writer.writerow(['Energy Supply Cost'] + annual_energy_supply_cost)
        writer.writerow(['Energy Cost']
                        + annual_energy)
        writer.writerow(['Capacity Cost']
                        + annual_capacity)

    annual_gas_dir = model_instance.inputs.RESULTS_DIR + r'\Emissions.csv'
    with open(annual_gas_dir, 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(['Year']
                        +  model_instance.model_years)

        # Gasoline Consumption
        writer.writerow(['CO2 emissions']
                        + CO2_emissions)
        writer.writerow(['NOX emissions']
                        + NOX_emissions)

        writer.writerow(['PM 10 emissions']
                        + PM10_emissions)

        writer.writerow(['SO2 emissions']
                        + SO2_emissions)

        writer.writerow(['VOC emissions']
                        + VOC_emissions)

    annual_gas_dir = model_instance.inputs.RESULTS_DIR + r'\annual_gas_consumption.csv'
    with open(annual_gas_dir, 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)

        # Header
        writer.writerow(['Year']
                        + model_instance.vehicles.gas_consumption_range)

        # Gasoline Consumption
        writer.writerow(['Gasoline Consumption (gallons)']
                        + annual_gas_consumption)
        writer.writerow(['Gasoline Consumption (MMBTU)']
                        + annual_gas_consumption_mmbtu)

        writer.writerow(['Gasoline Emissions (metric tons CO2)']
                        + annual_gas_consumption_co2)

        writer.writerow(['PHEV 10 Gasoline Consumption (gallons)']
                        + phev10_annual_gas_consumption)
        writer.writerow(['PHEV 10 Gasoline Consumption (MMBTU)']
                        + phev10_annual_gas_consumption_mmbtu)

        writer.writerow(['PHEV 10 Gasoline Emissions (metric tons CO2)']
                        + phev10_annual_gas_consumption_co2)

        writer.writerow(['PHEV 20 Gasoline Consumption (gallons)']
                        + phev20_annual_gas_consumption)
        writer.writerow(['PHEV 20 Gasoline Consumption (MMBTU)']
                        + phev20_annual_gas_consumption_mmbtu)

        writer.writerow(['PHEV 20 Gasoline Emissions (metric tons CO2)']
                        + phev20_annual_gas_consumption_co2)

        writer.writerow(['PHEV 40 Gasoline Consumption (gallons)']
                        + phev40_annual_gas_consumption)
        writer.writerow(['PHEV 40 Gasoline Consumption (MMBTU)']
                        + phev40_annual_gas_consumption_mmbtu)
        writer.writerow(['PHEV 40 Gasoline Emissions (metric tons CO2)']
                        + phev40_annual_gas_consumption_co2)

        writer.writerow(['BEV 100 Gasoline Consumption (gallons)']
                        + bev100_annual_gas_consumption)
        writer.writerow(['BEV 100 Gasoline Consumption (MMBTU)']
                        + bev100_annual_gas_consumption_mmbtu)

        writer.writerow(['BEV 100 Gasoline Emissions (metric tons CO2)']
                        + bev100_annual_gas_consumption_co2)

        writer.writerow(['EV Share (%)'] + ev_share)

def export_loadprofiles(model_instance, data, name):
    loadprofile_dir = model_instance.inputs.RESULTS_DIR + r'\%s_loadprofile.csv' % name

    with open(loadprofile_dir, 'w', newline ='') as csvfile:
        writer = csv.writer(csvfile)

        for row in data:
            writer.writerow(row)
