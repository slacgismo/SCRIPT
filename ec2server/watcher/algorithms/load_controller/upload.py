# entry to upload pre-generated models to the database

import load_control_algorithm

import argparse
import json
import psycopg2
from pathlib import Path
import os

parser = argparse.ArgumentParser()
parser.add_argument('--db_host', type=str, required=True)
parser.add_argument('--table_name', type=str, default='script_config_load_controller')
parser.add_argument('--postgres_db', type=str, required=True)
parser.add_argument('--postgres_user', type=str, required=True)
parser.add_argument('--postgres_password', type=str, required=True)
args = parser.parse_args()

MODELS_DIR = load_control_algorithm.MODELS_DIR
DB_HOST = args.db_host
TABLE_NAME = args.table_name
POSTGRES_DB = args.postgres_db
POSTGRES_USER = args.postgres_user
POSTGRES_PASSWORD = args.postgres_password
POSTGRES_PORT = '5432' # use the default port

# [CRITICAL] The following should only running after the database is initialized + county data should be inserted

conn = psycopg2.connect(
    host=DB_HOST,
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    port=POSTGRES_PORT
)

cur = conn.cursor()

total = 0

for filename in Path(MODELS_DIR).rglob('*_*/model.conf'):
    filepath = os.path.join(MODELS_DIR, filename)
    with open(filepath) as json_file:
        config = json.load(json_file)
    total += 1
    cur.execute("INSERT INTO {}".format(TABLE_NAME) + \
        " (county_id, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak," + \
        " rate_demand_peak, rate_demand_partpeak, rate_demand_overall)" + \
        " VALUES ('{}', {}, {}, {}, {}, {}, {})".format(
            config['county'], config['rate_energy_peak'], config['rate_energy_partpeak'], config['rate_energy_offpeak'],
            config['rate_demand_peak'], config['rate_demand_partpeak'], config['rate_demand_overall']))


# Make the changes to the database persistent
conn.commit()

# Close communication with the database
cur.close()
conn.close()

print('{} model(s) uploaded to the database successfully!'.format(total))
