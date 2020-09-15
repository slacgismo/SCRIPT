import csv
import pandas as pd


def createUploadData():
    data = pd.read_csv('sessions_clean.csv')
    county_names = data['County'].unique()
    county_session_count = data['County'].value_counts().tolist()
    county_total_energy = []
    county_peak_energy = []
    for county in county_names:
        county_total_energy.append(data.loc[data['County'] == county, 'Energy (kWh)'].sum())
        county_peak_energy.append(data.loc[data['County'] == county, 'Energy (kWh)'].max())
    county_data = pd.DataFrame()
    county_data['name'] = county_names
    county_data['total_session'] = county_session_count
    county_data['total_energy'] = county_total_energy
    county_data['peak_energy'] = county_peak_energy

    print(county_data.to_dict())
    return county_data.to_dict()

if __name__ == "__main__":
    something = createUploadData()
