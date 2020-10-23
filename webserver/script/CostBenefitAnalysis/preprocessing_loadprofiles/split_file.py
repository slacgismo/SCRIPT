'''
Author: Huai Jiang Robbie Shaw
Email: huai@ethree.com robbie@ethree.com
'''

from __future__ import division
import pandas as pd
import os
import numpy as np
from pathlib import Path 
from s3fs.core import S3FileSystem

def stock_rollover(adoption_start, adoption_end, vehicle_lifetime, population):
    
    new_sales = {}
    replacements = {}
    sales = {}

    new_sales[adoption_start] = population[adoption_start]

    for year in range(adoption_start, adoption_end + 1):
        if year == adoption_start:
            try:
                new_sales[year] = population[year] - population[year-1]
            except:
                new_sales[year] = 0
        else:
            new_sales[year] = population[year] - population[year-1]

    for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
        new_sales[year] = 0.

    first_replacement_year = adoption_start + vehicle_lifetime
    for year in range(adoption_start, first_replacement_year):
        replacements[year] = 0.

    for year in range(first_replacement_year, adoption_end + 1):
        replacements[year] = \
            new_sales[year - vehicle_lifetime] + replacements[year - vehicle_lifetime]

    for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
        replacements[year] = 0.

    for year in range(adoption_start, adoption_end + vehicle_lifetime):
        sales[year] = new_sales[year] + replacements[year]

    for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
        try:
            population[year] = population[year-1] - sales[year - vehicle_lifetime]
        except:
            population[year] = population[year - 1]

    return population


def hourly(array):
    return np.mean(np.reshape(array, (int(len(array) / 60), 60)), axis=1) #depending on the unit


def split_file(county, scenarios={'Scenario 1': 'BaseCase'}, controlled_types=['uncontrolled'], years=['2025']):

    s3 = S3FileSystem(anon=False)
    bucket = 's3://script.control.tool'
    path = Path(__file__).parent.resolve()

    # Input Loads - currently only setting up for weekday loads
    WEEKDAY_SLAC_DATA_PATH = str(path)+'/inputs/weekdays/'
    weekday_load_list = list(WEEKDAY_SLAC_DATA_PATH)

    # Driver Counts Path
    driver_counts_path = 'Driver Counts'

    # Adoption File - This file must correspond to the scenario selected.
    adoption_path = 'Adoption Files/vehicle_adoption base case.xlsx'

    combined_output = pd.DataFrame()

    output_dictionary = {}

    Charger_types = ['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Public L2', 'Fast', 'Total']
    for field_name in Charger_types:
        output_dictionary[field_name] = pd.DataFrame()

    for Scenario in scenarios.values():
        for Management in controlled_types:
            for county in county:
                for SLAC_Year in years:

                    # Read SLAC Driver Count
                    Driver_counts_file_name = "{}_{}_weekday__driver_counts.csv".format(Scenario, SLAC_Year)
                    driver_count_df = pd.read_csv("{}/{}/{}".format(bucket, driver_counts_path, Driver_counts_file_name))

                    if Scenario in ['WorkPublic', 'FastPublic', 'Work', 'Equity']:
                        weekday_file_name = "{}_rescaled_{}_weekday_{}_county_{}_load.csv".format(Scenario, SLAC_Year, county, Management)
                    else:
                        weekday_file_name = "{}_{}_weekday_{}_county_{}_load.csv".format(Scenario, SLAC_Year, county, Management)

                    driver_count = float(driver_count_df.loc[driver_count_df['County'] == county]['Num Drivers'])

                    adoption_spreadsheet_df = \
                        pd.read_excel(f"{bucket}/{adoption_path}", sheet_name=county).set_index(['year'])[' BEV_population']

                    weekday_all = pd.read_csv(os.path.join(WEEKDAY_SLAC_DATA_PATH,weekday_file_name))
                    day_type = pd.read_csv(os.path.join(str(path),'day_type.csv'))

                    weekday_all = weekday_all.drop(list(weekday_all)[0],axis=1)
                    col_names = list(weekday_all.columns)

                    for field_name in col_names:
                        weekday_array = np.array(weekday_all[field_name])
                        weekday_aggregated = hourly(weekday_array) # convert from 1-min to 1-hour

                        output = []
                        for i in range(day_type.shape[0]):
                            if day_type['DayType'][i] == 1:
                                output.append(weekday_aggregated)
                            else:
                                output.append(weekday_aggregated)

                        annual_output = output * 52
                        output = np.array(annual_output)
                        output = np.append(output, output[0])
                        output = np.reshape(output, 8760)
                        output = pd.DataFrame(output, columns = {SLAC_Year})

                        per_vehicle_results = output/driver_count

                        if SLAC_Year == "2025":
                            for year in range(2019, 2031):
                                output_dictionary[field_name][year] = per_vehicle_results[SLAC_Year] * adoption_spreadsheet_df.loc[year]/1000
                        
                        elif SLAC_Year == "2030":
                            year = 2030
                            output_dictionary[field_name][year] = per_vehicle_results[SLAC_Year] * adoption_spreadsheet_df.loc[year]/1000

                        stock_rollover_output = stock_rollover(2019, 2030, 11, output_dictionary[field_name])

                        stock_rollover_output.to_csv(os.path.join(
                            str(path), "outputs",  "{}_{}_{}_{}_load.csv".format(
                                Scenario, county, field_name, Management)),index = True)
