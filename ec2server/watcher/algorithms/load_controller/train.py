# TODO: entry to train and generate models

import load_control_algorithm

import argparse

CHARGE_RATE = 6.6 # TODO: hardcoded?

parser = argparse.ArgumentParser()
parser.add_argument('--county', type=str, nargs='+', help='Please replace space with dash(-)', default=['Santa-Clara',])
parser.add_argument('--rate_energy_peak', type=float, default=0.16997)
parser.add_argument('--rate_energy_partpeak', type=float, default=0.12236)
parser.add_argument('--rate_energy_offpeak', type=float, default=0.09082)
parser.add_argument('--rate_demand_peak', type=float, default=21.23)
parser.add_argument('--rate_demand_partpeak', type=float, default=5.85)
parser.add_argument('--rate_demand_overall', type=float, default=19.10)
parser.add_argument('--s3_session_path', type=str, help='An s3 .csv file or a prefix', default='s3://script.chargepoint.data/clean/sessions_paired.csv')
parser.add_argument('--s3_interval_path', type=str, help='An s3 .csv file or a prefix', default='s3://script.chargepoint.data/clean/intervals_paired.csv')
parser.add_argument('--model_name', type=str, help='Prefix of model name', default='test')
args = parser.parse_args()

county_list = [county.replace('-', ' ') for county in args.county]
rate_energy_peak = args.rate_energy_peak
rate_energy_partpeak = args.rate_energy_partpeak
rate_energy_offpeak = args.rate_energy_offpeak
rate_demand_peak = args.rate_demand_peak
rate_demand_partpeak = args.rate_demand_partpeak
rate_demand_overall = args.rate_demand_overall
s3_session_path = args.s3_session_path
s3_interval_path = args.s3_interval_path
model_name = args.model_name

# cache data(run when data collection changes)
load_control_algorithm.LoadControlAlgorithm.cache_data(s3_session_path, s3_interval_path)

# train and generate models
for county in county_list:
    lca = load_control_algorithm.LoadControlAlgorithm(county,
                                                        rate_energy_peak,
                                                        rate_energy_partpeak,
                                                        rate_energy_offpeak,
                                                        rate_demand_peak,
                                                        rate_demand_partpeak,
                                                        rate_demand_overall)
    lca.generate_profiles(50, 200, CHARGE_RATE)
    lca.generate_model('{}_{}'.format(model_name, county.replace(' ', '_')))
