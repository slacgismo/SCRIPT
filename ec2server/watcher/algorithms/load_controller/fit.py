# entry to fit data using existing models for Celery
from celery import shared_task, current_task
from .load_control_algorithm import LoadControlAlgorithm
from pathlib import Path
import os
import pickle
from sklearn.linear_model import LinearRegression

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
MODELS_DIR = os.path.join(HOME_DIR, 'models')

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
            # TODO: check if the results have been cached in the database
            # TODO: read data from s3
            # TODO: fit
            # TODO: cache the results to the database
            # success
            return 'success!'