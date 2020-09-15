import boto3
import json
import psycopg2
import numpy as np
import pandas as pd
import csv


class UploadToPostgres():
    def __init__(self):
        with open("postgres_info.json") as json_file:
            postgres_info = json.load(json_file)

        self.db_host = postgres_info["DB_HOST"]
        self.table_county = "script_county"
        self.table_zipcode = "script_zip_code"
        self.postgres_db = postgres_info['POSTGRES_DB']
        self.postgres_user = postgres_info['POSTGRES_USER']
        self.postgres_password = postgres_info['POSTGRES_PASSWORD']


    def createCountyUploadData(self, s3_path):
        ''' cleans data before and returns dictionary before uploading to db'''

        data = pd.read_csv(s3_path)
        county_names = data['County'].unique()
        # number of county entries in the dataset
        county_session_count = data['County'].value_counts().tolist()

        county_total_energy = []
        county_peak_energy = []
        county_zip_codes = []

        # loops on the unique county names to gather corresponding data
        for x in range(len(county_names)):
            # kWh - so takes average data used
            county_total_energy.append(data.loc[data['County'] == county_names[x], 'Energy (kWh)'].sum()/county_session_count[x])
            county_peak_energy.append(data.loc[data['County'] == county_names[x], 'Energy (kWh)'].max())
            # create a list of zipcodes for each county
            county_zip_codes.append(data.loc[data['County'] == county_names[x], 'Zip Code'].drop_duplicates())
            county_names[x] = county_names[x].replace(' County', "")

        county_data = pd.DataFrame()
        county_data['name'] = county_names
        county_data['total_session'] = county_session_count
        county_data['total_energy'] = county_total_energy
        county_data['peak_energy'] = county_peak_energy
        county_data['zip_code'] = county_zip_codes

        return county_data.to_dict()


    def run(self):

        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port="5432"
        )

        county_data = self.createCountyUploadData("s3://script.chargepoint.data/clean/sessions_clean.csv")
        cur = conn.cursor()

        for x in range(len(county_data["name"])):
            cur.execute("INSERT INTO " + self.table_county + \
                " (name, total_session, total_energy, peak_energy)" + \
                " VALUES (%s, %s, %s, %s)",
                (
                    county_data["name"][x],
                    county_data["total_session"][x],
                    county_data["total_energy"][x],
                    county_data["peak_energy"][x]
                )
            )
            for zipcode in county_data["zip_code"][x]:
                cur.execute("INSERT INTO " + self.table_zipcode + " (code, county)" + " VALUES (%s, %s)",
                    (
                        str(zipcode),
                        str(county_data["name"][x])
                    )
                )

        conn.commit()
        conn.close()

if __name__ == "__main__":
    client = UploadToPostgres()
    client.run()
