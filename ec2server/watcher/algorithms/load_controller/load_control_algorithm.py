import pandas as pd
import numpy as np
import boto3
import cvxpy as cvx
import json
import os
import pytz
import pickle
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
    def new_sessions_intervals(self, county, num_sessions):
        """generate new session data and related interval data"""
        zip_options = get_county_zipcodes_from_local(county)
        file_options = []
        for zipcode in zip_options:
            file_name = os.path.join(SESSIONS_DIR, '{}.csv'.format(zipcode))
            if os.path.exists(file_name):
                file_options.append(file_name)
        print('Have ', len(file_options), ' zips in this county cached')
        ct = 0
        len_session = 0
        while ((len_session == 0) & (ct < len(file_options))):
            zipcode_file = np.random.choice(file_options)
            df_sessions = pd.read_csv(zipcode_file)
            df_sessions = df_sessions[df_sessions['POI Category'] == 'Workplace'].reset_index(drop=True)
            df_sessions = df_sessions[df_sessions['Max Power'] <= 10].reset_index(drop=True) # Not fast charging
            len_session = len(df_sessions)
            ct += 1
        df_intervals = pd.read_csv(os.path.join(INTERVALS_DIR, '{}.csv'.format(zipcode)))
        chosen_session_indexes = np.random.choice(df_sessions.index, num_sessions)
        return df_sessions, df_intervals, chosen_session_indexes

    @staticmethod
    def uncontrolled_load(num_sessions, chosen_session_indexes, df_sessions, df_intervals, charge_rate):
        """Calculate uncontrolled load"""
        power = np.zeros((96, num_sessions))
        arrival_inds = np.zeros((num_sessions, ))
        departure_inds = np.zeros((num_sessions, ))
        for session_num in range(num_sessions):
            session = df_sessions.loc[chosen_session_indexes[session_num], 'Session ID']
            interval_data = df_intervals[df_intervals['Session ID']==session]
            for i in interval_data.index:
                hour = int(interval_data.loc[i, 'Interval Start Time (Local)'][11:13])
                minute = int(interval_data.loc[i, 'Interval Start Time (Local)'][14:16])
                timestep_96 = hour * 4 + int(minute / 15)
                power[timestep_96, session_num] = float(interval_data.loc[i, 'Average Power'])
            if power[0, session_num] == 0:
                if len(np.where(power[:, session_num] > 0)[0]) > 0:
                    arrival_inds[session_num] = np.where(power[:, session_num] > 0)[0][0]
                    if np.where(power[:, session_num] > 0)[0][-1] + 1 < 96:
                        departure_inds[session_num] = np.where(power[:, session_num] > 0)[0][-1] + 1
                    else: 
                        departure_inds[session_num] = 0
            else:
                if len(np.where(power[:, session_num] == 0)[0]) > 0:
                    arrival_inds[session_num] = np.max(np.where(power[:, session_num] == 0)[0]) + 1
                    if arrival_inds[session_num] == 96:
                        arrival_inds[session_num] = 0
                    departure_inds[session_num] = np.min(np.where(power[:, session_num] == 0)[0])
        energies = 0.25 * np.sum(power, axis=0)
        return power, arrival_inds, departure_inds, energies

    def controlled_load(self,
                        num_sessions,
                        charge_rate,
                        arrival_inds,
                        departure_inds,
                        power,
                        energies,
                        energy_prices, 
                        rate_demand_peak,
                        rate_demand_partpeak,
                        rate_demand_overall,
                        peak_inds,
                        partpeak_inds):
        """Predict controlled load"""
        schedule = cvx.Variable((96, num_sessions))
        obj = cvx.matmul(cvx.sum(schedule, axis=1),  energy_prices.reshape((np.shape(energy_prices)[0], 1)))
        obj += rate_demand_overall*cvx.max(cvx.sum(schedule, axis=1))
        obj += rate_demand_overall*cvx.max(cvx.sum(schedule, axis=1))
        obj += rate_demand_peak*cvx.max(cvx.sum(schedule[peak_inds, :], axis=1))
        obj += rate_demand_partpeak*cvx.max(cvx.sum(schedule[partpeak_inds, :], axis=1))

        constraints = [schedule >= 0]
        for i in range(num_sessions):
            constraints += [schedule[:, i] <= np.maximum(np.max(power[:, i]), charge_rate)]
            if departure_inds[i] >= arrival_inds[i]:
                if arrival_inds[i] > 0:
                    constraints += [schedule[np.arange(0, int(arrival_inds[i])), i] <= 0]
                if departure_inds[i] < 96:
                    constraints += [schedule[np.arange(int(departure_inds[i]), 96), i] <= 0]
            else:
                constraints += [schedule[np.arange(int(departure_inds[i]), int(arrival_inds[i])), i] <= 0]

        energies = 0.25 * np.sum(power, axis=0)
        max_energies = np.zeros((num_sessions, ))
        for i in range(num_sessions):
            if departure_inds[i] >= arrival_inds[i]:
                max_energies[i] = 0.25 * charge_rate * (departure_inds[i] - arrival_inds[i])
            else:
                max_energies[i] = 0.25 * charge_rate * ((departure_inds[i]) + (96 - arrival_inds[i]))
        where_violation = np.where((max_energies-energies) < 0)[0]

        energies[where_violation] = max_energies[where_violation]
        constraints += [0.25*cvx.sum(schedule, axis=0) == energies]
        prob = cvx.Problem(cvx.Minimize(obj), constraints)
        result = prob.solve(solver=cvx.MOSEK)
        return schedule.value, power, len(where_violation)

    def generate_profiles(self, num_run, num_sessions, charge_rate):
        """Generate profiles as training data"""
        peak_inds = np.arange(int(12 * 4), int(18 * 4))
        partpeak_inds = np.concatenate((np.arange(int(8.5 * 4), int(12 * 4)), np.arange(int(18 * 4), int(21.5 * 4))))
        energy_prices = np.concatenate((np.repeat(rate_energy_offpeak, int(8.5 * 4)),
                                        np.repeat(rate_energy_partpeak, int(3.5*4)),
                                        np.repeat(rate_energy_peak, int(6 * 4)),
                                        np.repeat(rate_energy_partpeak, int(3.5 * 4)), 
                                        np.repeat(rate_energy_offpeak, int(2.5 * 4))))

        self.baseline_profiles = np.zeros((96, num_runs))
        self.controlled_profiles = np.zeros((96, num_runs))
        saved_indices = np.zeros((num_sessions, num_runs))
        list_violations = []
        for i in range(num_runs):
            print('On run: ', i)
            df_sessions, df_intervals, chosen_session_indexes = self.new_df_and_sessions(county, num_sessions) #this first! 
            saved_indices[:, i] = chosen_session_indexes
            power, arrival_inds, departure_inds, energies = self.uncontrolled_load(num_sessions, chosen_session_indexes, df_sessions, df_intervals, charge_rate)
            schedule, power, violations = self.controlled_load(num_sessions,
                                                                charge_rate,
                                                                arrival_inds,
                                                                departure_inds,
                                                                power,
                                                                energies,
                                                                energy_prices, 
                                                                rate_demand_peak,
                                                                rate_demand_partpeak,
                                                                rate_demand_overall,
                                                                peak_inds,
                                                                partpeak_inds)
            self.baseline_profiles[:, i] = np.sum(power, axis=1)
            self.controlled_profiles[:, i] = np.sum(schedule, axis=1)
            list_violations.append(violations)

    def generate_model(self, dir_name):
        """Generate Linear Regression model"""
        # Split data into train and test sets
        X_train, X_test, y_train, y_test = train_test_split(np.transpose(self.baseline_profiles),
                                                            np.transpose(self.controlled_profiles),
                                                            test_size=0.2,
                                                            random_state=42)

        # Define and fit classifier
        clf = LinearRegression()
        clf.fit(X_train, y_train)

        # Score on test set
        clf.score(X_test, y_test)
        
        # Pretty good R^2 value with the linear regression model
        y_predicted = clf.predict(X_test)
        print('Prediction: \n', y_predicted)

        # persist config
        dir_path = os.path.join(MODELS_DIR, dir_name)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        config = {
            'county': self.county,
            'rate_energy_peak': self.rate_energy_peak,
            'rate_energy_partpeak': self.rate_energy_partpeak,
            'rate_energy_offpeak': self.rate_energy_offpeak,
            'rate_demand_peak': self.rate_demand_peak,
            'rate_demand_partpeak': self.rate_demand_partpeak,
            'rate_demand_overall': self.rate_demand_overall
        }
        with open(os.path.join(dir_path, 'model.conf'), 'w') as conf_file:
            json.dump(config, conf_file)

        # persist model
        with open(os.path.join(dir_path, 'model.clf'), 'ab') as clf_file:
            pickle.dump(clf, clf_file)

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
