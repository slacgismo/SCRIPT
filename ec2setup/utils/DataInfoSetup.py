import boto3
import json
import psycopg2
import pandas as pd
import numpy as np

with open('postgres_info.json') as json_file:
    postgres_info = json.load(json_file)

# store all county into postgres table
db_host = postgres_info['DB_HOST']
county_table_name = "script_county"
postgres_db = postgres_info['POSTGRES_DB']
postgres_user = postgres_info['POSTGRES_USER']
postgres_password = postgres_info['POSTGRES_PASSWORD']


conn = psycopg2.connect(
    host=db_host,
    dbname=postgres_db,
    user=postgres_user,
    password=postgres_password,
    port='5432'
)

cur = conn.cursor()

zip_county_lookup = pd.read_csv('zip_county_lookup.json')
zip_county_lookup['Zip Code'] = zip_county_lookup['Zip Code'].astype(int)
county_list = np.unique(zip_county_lookup['County'].values)

for county_name in county_list:
    residents_num = 100000
    cur.execute("INSERT INTO " + county_table_name + \
        " (name, residents)" + \
        " VALUES (%s, %s)",
        (
            county_name, str(residents_num)
        )
    )

print('Inserting county info finished...')
# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()
