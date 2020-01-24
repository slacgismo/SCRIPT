# entry to fit data using existing models for Celery
from celery import shared_task, current_task
from .load_control_algorithm import LoadControlAlgorithm
from pathlib import Path
import os
import pickle
import json
import psycopg2
from sklearn.linear_model import LinearRegression

# [CRITICAL] ec2server should running with configured environment variables
DB_HOST = os.getenv('DB_HOST')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
POSTGRES_PORT = '5432' # use the default port

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
MODELS_DIR = os.path.join(HOME_DIR, 'models')

CONFIG_TABLE_NAME = 'script_config_load_controller'
ALGORITHM_TABLE_NAME = 'script_algorithm_load_controller'


def get_config_id(config):
    cur.execute("SELECT id FROM {}".format(CONFIG_TABLE_NAME) + \
        " WHERE county_id='{}' and".format(config['county']) + \
        " rate_energy_peak={} and".format(config['rate_energy_peak']) + \
        " rate_energy_partpeak={} and".format(config['rate_energy_partpeak']) + \
        " rate_energy_offpeak={} and".format(config['rate_energy_offpeak']) + \
        " rate_demand_peak={} and".format(config['rate_demand_peak']) + \
        " rate_demand_partpeak={} and".format(config['rate_demand_partpeak']) + \
        " rate_demand_overall={}".format(config['rate_demand_overall'])
    )
    config_id = cur.fetchone()[0] # it shouldn't be None
    return config_id


def check_algorithm_result(config_id):
    cur.execute("SELECT uncontrolled_load, controlled_load FROM {}".format(ALGORITHM_TABLE_NAME) + \
        " WHERE config_id={}".format(config_id)
    )
    res = cur.fetchone()
    return res


def insert_result(uncontrolled_load, controlled_load, config_id):
    cur.execute("INSERT INTO {}".format(ALGORITHM_TABLE_NAME) + \
        " (uncontrolled_load, controlled_load, config_id) VALUES" + \
        " ('{}', '{}', {})".format(uncontrolled_load, controlled_load, config_id)
    )


def fit():
    # TODO: fit
    baselien_profiles, controlled_profiles = LoadControlAlgorithm.fit()

    baseline_profiles_list = []
    controlled_profiles_list = []

    start_hour = 0
    start_minute = 0

    lines = len(baseline_profiles / 4)
    for line in range(lines):
        hour_str = str((start_hour + line % 4)% 24)
        minute = 15 * (line % 4)
        if minute is 0:
            minute_str = '00'
        else:
            minute_str = str(minute)

        self.total_energy += int(baseline_profiles[line][self.num_of_run - 1])
        baseline_profiles_list.append(
            {
                'time': hour_str + ':' + minute_str,
                'load': str(baseline_profiles[line][self.num_of_run - 1])
            }
        )

        controlled_profiles_list.append(
            {
                'time': hour_str + ':' + minute_str,
                'load': str(controlled_profiles[line][self.num_of_run - 1])
            }
        )
    
    return baseline_profiles_list, controlled_profiles_list


# TODO: there should be two counties: model_county and data_county
@shared_task
def load_control_fit(county, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak, rate_demand_peak, rate_demand_partpeak, rate_demand_overall):
    target_config = {
        'county': county,
        'rate_energy_peak': rate_energy_peak,
        'rate_energy_partpeak': rate_energy_partpeak,
        'rate_energy_offpeak': rate_energy_offpeak,
        'rate_demand_peak': rate_demand_peak,
        'rate_demand_partpeak': rate_demand_partpeak,
        'rate_demand_overall': rate_demand_overall
    }
    county_str = county.replace(' ', '_')
    for filename in Path(MODELS_DIR).rglob('*_{}/model.conf'.format(county_str)):
        filepath = os.path.join(MODELS_DIR, filename)
        with open(filepath) as json_file:
            config = json.load(json_file)
        if config == target_config:
            modelpath = filepath.rreplace('.conf', '.clf', 1)
            with open(modelpath, 'rb') as clf_file:
                clf = pickle.load(clf_file)
            
            # setup connection
            conn = psycopg2.connect(
                host=DB_HOST,
                dbname=POSTGRES_DB,
                user=POSTGRES_USER,
                password=POSTGRES_PASSWORD,
                port=POSTGRES_PORT
            )
            cur = conn.cursor()
            
            # get config_id
            config_id = get_config_id(target_config)
            # check if the results have been cached in the database
            # TODO: this part has a duplicate in views.py!!!!
            res = check_algorithm_result(config_id)
            ret = None
            if res is None:
                # TODO: read data from s3
                # TODO: fit
                uncontrolled_load, controlled_load = fit(modelpath, county, data_county)
                # cache the results to the database
                insert_result(json.dumps(uncontrolled_load), json.dumps(controlled_load), config_id)
                ret = (uncontrolled_load, controlled_load)
            else:
                ret = res # (uncontrolled_load, controlled_load)

            # close connection
            conn.commit()
            cur.close()
            conn.close()

            return ret
