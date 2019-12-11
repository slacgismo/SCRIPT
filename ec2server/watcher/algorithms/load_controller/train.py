# TODO: entry to train and generate models

import load_control_algorithm

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--county', type=str, nargs='+', help='Please replace space with dash(-)')
parser.add_argument('--rate_energy_peak', type=float)
parser.add_argument('--rate_energy_partpeak', type=float)
parser.add_argument('--rate_energy_offpeak', type=float)
parser.add_argument('--rate_demand_peak', type=float)
parser.add_argument('--rate_demand_partpeak', type=float)
parser.add_argument('--rate_demand_overall', type=float)
parser.add_argument('--s3_path', type=str, help='An s3 .csv file or a prefix')
args = parser.parse_args()

county_list = [county.replace('-', ' ') for county in args.county]
rate_energy_peak = args.rate_energy_peak
rate_energy_partpeak = args.rate_energy_partpeak
rate_energy_offpeak = args.rate_energy_offpeak
rate_demand_peak = args.rate_demand_peak
rate_demand_partpeak = args.rate_demand_partpeak
rate_demand_overall = args.rate_demand_overall
s3_path = args.s3_path

# cache data
load_control_algorithm.LoadControlAlgorithm.cache_data(s3_path)

# TODO: train and generate models
