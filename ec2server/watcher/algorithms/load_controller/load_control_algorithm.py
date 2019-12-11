import pandas as pd
import numpy as np
import boto3
import cvxpy as cvx
import json
import os
import pytz
from datetime import datetime

HOME_DIR = os.path.dirname(os.path.realpath(__file__))
DATA_DIR = os.path.join(HOME_DIR, 'data')
MODELS_DIR = os.path.join(HOME_DIR, 'models')
SESSIONS_DIR = os.path.join(DATA_DIR, 'sessions')
INTERVALS_DIR = os.path.join(DATA_DIR, 'intervals')


class LoadControlAlgorithm:
    def __init__(self,
                county,
                rate_energy_peak,
                rate_energy_partpeak,
                rate_energy_offpeak,
                rate_demand_peak,
                rate_demand_partpeak,
                rate_demand_overall):
        self.county = county
        self.rate_energy_peak = rate_energy_peak
        self.rate_energy_partpeak = rate_energy_partpeak
        self.rate_energy_offpeak = rate_energy_offpeak
        self.rate_demand_peak = rate_demand_peak
        self.rate_demand_partpeak = rate_demand_partpeak
        self.rate_demand_overall = rate_demand_overall
        self.zipcodes = get_county_zipcodes_from_local()
        self.data = get_county_data_from_local()

    @staticmethod
    def get_zipcodes_from_local():
        """Read all zip codes from local files"""
        zip_county_lookup = pd.read_csv(os.path.join(DATA_DIR, 'zip_county_lookup.json'))
        return zip_county_lookup['Zip Code'].astype(int).values

    @staticmethod
    def get_county_zipcodes_from_local(county):
        """Read all zip codes of a certain county from local files"""
        zip_county_lookup = pd.read_csv(os.path.join(DATA_DIR, 'zip_county_lookup.json'))
        zip_county_lookup['Zip Code'] = zip_county_lookup['Zip Code'].astype(int)
        zip_options = zip_county_lookup[zip_county_lookup['County'] == county]['Zip Code'].values
        return zip_options

    def get_county_data_from_local(self):
        """Read all data of all zipcodes of a certain county from local files"""
        pass

    @staticmethod
    def new_df_and_sessions(self, county, num_sessions):
        """generate new session data and related interval data"""
        zip_options = get_county_zipcodes_from_local(county)
        file_options = []

        for zipcode in zip_options:
            file_name = os.path.join(SESSIONS_DIR, '{}.csv'.format(zipcode))
            if os.path.exists(file_name):
                file_options.append(file_name)

        print('Have ', len(file_options), ' zips in this county cached')

        ct = 0
        len_df = 0
        while ((len_df == 0) & (ct < len(file_options))):
            zipcode_file = np.random.choice(file_options)
            df = pd.read_csv(zipcode_file)
            df = df[df['POI Category'] == 'Workplace'].reset_index(drop=True)
            df = df[df['Max Power'] <= 10].reset_index(drop=True) # Not fast charging
            len_df = len(df)
            ct += 1

        df_intervals = pd.read_csv(os.path.join(INTERVALS_DIR, '{}.csv'.format(zipcode)))
        chosen_sessions = np.random.choice(df.index, num_sessions)

        return df, df_intervals, chosen_sessions

    @staticmethod
    def uncontrolled_load(df_sessions, df_intervals):
        """Calculate uncontrolled load"""
        pass

    def controlled_load(self):
        pass

    def generate_models(self):
        pass

    @staticmethod
    def cache_data(s3_session_path, s3_interval_path):
        """download all session and interval data from s3 and categorize data by zipcodes"""
        session_list = []
        if s3_session_path.endswith('.csv'):
            session_list.append(s3_session_path)
        else:
            s3_resource = boto3.resource('s3')
            bucket_name, s3_prefix = s3_session_path.split('/', 1)
            s3_bucket = s3_resource.Bucket(bucket_name)
            objs = s3_bucket.objects.filter(Prefix=bucket_prefix)
            for obj in objs:
                session_list.append(os.path.join(bucket_name, obj.key))

        # download and merge into one df
        df_list = []
        for csv_path in session_list:
            df_list.append(pd.read_csv(csv_path))
        df_sessions = pd.concat(df_list)

        # categorize by zipcodes and save to ./data
        if not os.path.exists(SESSIONS_DIR):
            os.makedirs(SESSIONS_DIR)
        zipcodes = get_zipcodes_from_local()
        session_ids = {}
        for zip_code in zipcodes:
            df = df_sessions[df_sessions['Zip Code'] == zip_code]
            session_ids[zip_code] = df['Session ID'].values
            file_path = os.path.join(SESSIONS_DIR, '{}.csv'.format(zip_code))
            df.to_csv(file_path, index=False)

        interval_list = []
        if s3_interval_path.endswith('.csv'):
            interval_list.append(s3_interval_path)
        else:
            s3_resource = boto3.resource('s3')
            bucket_name, s3_prefix = s3_interval_path.split('/', 1)
            s3_bucket = s3_resource.Bucket(bucket_name)
            objs = s3_bucket.objects.filter(Prefix=bucket_prefix)
            for obj in objs:
                interval_list.append(os.path.join(bucket_name, obj.key))

        # download and merge into one df
        df_list = []
        for csv_path in interval_list:
            df_list.append(pd.read_csv(csv_path))
        df_intervals = pd.concat(df_list)

        # categorize by zipcodes and save to ./data
        if not os.path.exists(INTERVALS_DIR):
            os.makedirs(INTERVALS_DIR)
        zipcodes = get_zipcodes_from_local()
        for zip_code in zipcodes:
            ids = session_ids[zip_code]
            df = intervals[df_intervals['Session ID'].isin(ids)]
            file_path = os.path.join(INTERVALS_DIR, '{}.csv'.format(zip_code))
            df.to_csv(file_path, index=False)
