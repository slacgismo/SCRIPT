import boto3
import json
import psycopg2
import numpy as np
import pandas as pd
import csv

class UploadToPostgres():
    def __init__(
        self
    ):
        with open('postgres_info.json') as json_file:
            postgres_info = json.load(json_file)
        
        self.db_host = postgres_info['DB_HOST']
        self.table_county = "script_county"
        self.table_zipcode = "script_zip_code"
        self.postgres_db = postgres_info['POSTGRES_DB']
        self.postgres_user = postgres_info['POSTGRES_USER']
        self.postgres_password = postgres_info['POSTGRES_PASSWORD']

    def run(self):

        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        cur = conn.cursor()

        self.zip_county_lookup = pd.read_csv('zip_county_lookup.json')

        self.county_list = np.unique(self.zip_county_lookup['County'].values)

        for county in self.county_list:

            cur.execute("SELECT * FROM "+self.table_county + " WHERE " + "name = \'" + county + "\'")

            county_exists = cur.fetchone()

            if not county_exists:
                cur.execute("INSERT INTO " + self.table_county + \
                    " (name, total_session, total_energy, peak_energy)" + \
                    " VALUES (%s, %s, %s, %s)",
                    (
                        county, "0", "0", "0"
                    )
                )

        conn.commit()

        with open('zip_county_lookup.json', 'r') as read_obj:
            reader = csv.DictReader(read_obj)
            for row in reader:
                zip_code = int(float(str((row['Zip Code']))))
                cur.execute("INSERT INTO " + self.table_zipcode + \
                    " (code, county)" + \
                        " VALUES (%s, %s)",
                        (
                            str(zip_code), str(row['County'])
                        )
                    )
        
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()

if __name__ == "__main__":
    client = UploadToPostgres()
    client.run()