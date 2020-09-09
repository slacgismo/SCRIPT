import pandas as pd
import numpy as np
import boto3
import cvxpy as cvx
import json
import os
import pytz
from datetime import datetime
from script.SmartCharging.UploadToPostgres import *
from django.conf import settings

#from SmartChargingFitting import *

s3 = boto3.resource('s3')
sca_dir = settings.BASE_DIR[:-3]

class SmartChargingAlgorithm:
    def __init__(self, s3_bucket_name):
        self.s3_bucket_name = s3_bucket_name
        self.zip_county_lookup = {}
        self.county_list = []
        self.county = ''
        self.rate_energy_peak = ''
        self.rate_energy_partpeak = ''
        self.rate_energy_offpeak = ''
        self.rate_demand_peak = ''
        self.rate_demand_partpeak = ''
        self.rate_demand_overall = ''

        # load data from S3
        self.load_county_data_from_local()


    def load_county_data_from_S3(self):
        """
            load data from S3 and save to local
        """
        self.zip_county_lookup = pd.read_csv('s3://script.forecast.inputsoutputs/zip_county_lookup_cleaned.csv')
        self.zip_county_lookup['Zip Code'] = self.zip_county_lookup['Zip Code'].astype(int)
        self.county_list = np.unique(self.zip_county_lookup['County'].values)
        print('County options: ', self.county_list)

    def load_county_data_from_local(self):
        """
            Read from local
        """
        self.zip_county_lookup = pd.read_csv(sca_dir + 'script/SmartCharging/zip_county_lookup.json')
        self.zip_county_lookup['Zip Code'] = self.zip_county_lookup['Zip Code'].astype(int)

        self.county_list = np.unique(self.zip_county_lookup['County'].values)
        print('County options: ', self.county_list)

    def new_df_and_sessions(self, county, num_sessions):
        """
            generate new df and sessions data
        """
        bucket = s3.Bucket(self.s3_bucket_name)
        zip_options = self.zip_county_lookup[self.zip_county_lookup['County']==county]['Zip Code'].values
        file_options = []

        for zipcode in zip_options:
            file_name = 'clean/Reduced/By_ZipCode/evsezip' + str(zipcode) + '_sessions.csv'
            # check if have data for this zip
            have_data = False
            objs = list(bucket.objects.filter(Prefix=file_name))
            if len(objs) > 0 and objs[0].key == file_name:
                file_options.append(file_name)

        print('Have ', len(file_options), ' zips in this county to pull from')

        ct = 0
        len_df = 0
        while ((len_df==0) & (ct < len(file_options))):
            zipcode_file = np.random.choice(file_options)
            df = pd.read_csv('s3://' + self.s3_bucket_name + '/' + zipcode_file)
            df = df[df['POI Category']=='Workplace'].reset_index(drop=True)
            df = df[df['Max Power']<=10].reset_index(drop=True) # Not fast charging
            len_df = len(df)
            ct += 1

        df_intervals = pd.read_csv('s3://' + self.s3_bucket_name + '/' + zipcode_file[:37] + '_intervals.csv')

        chosen_sessions = np.random.choice(df.index, num_sessions)

        return df, df_intervals, chosen_sessions

    def uncontrolled_load(self, num_sessions, chosen_sessions, df, df_intervals, charge_rate):
        """
            Calculate uncontrolled load
        """
        power = np.zeros((96, num_sessions))
        arrival_inds = np.zeros((num_sessions, ))
        departure_inds = np.zeros((num_sessions, ))
        for session_num in range(num_sessions):
            session = df.loc[chosen_sessions[session_num], 'Session ID']
            interval_data = df_intervals[df_intervals['Session ID']==session]
            for i in interval_data.index:
                hour = int(interval_data.loc[i, 'Interval Start Time (Local)'][11:13])
                minute = int(interval_data.loc[i, 'Interval Start Time (Local)'][14:16])
                timestep_96 = hour*4 + int(minute/15)
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
        energies = 0.25*np.sum(power, axis=0)

        return power, arrival_inds, departure_inds, energies

    def controlled_load(self, num_sessions, charge_rate, arrival_inds, departure_inds, power, energies, energy_prices,
                        rate_demand_peak, rate_demand_partpeak, rate_demand_overall, peak_inds, partpeak_inds):
        """
            Predict controlled load
        """
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

        energies = 0.25*np.sum(power, axis=0)
        max_energies = np.zeros((num_sessions, ))
        for i in range(num_sessions):
            if departure_inds[i] >= arrival_inds[i]:
                max_energies[i] = 0.25*charge_rate*(departure_inds[i]-arrival_inds[i])
            else:
                max_energies[i] = 0.25*charge_rate*((departure_inds[i])+(96-arrival_inds[i]))
        where_violation = np.where((max_energies-energies)<0)[0]

        energies[where_violation] = max_energies[where_violation]
        constraints += [0.25*cvx.sum(schedule, axis=0)==energies]

        prob = cvx.Problem(cvx.Minimize(obj), constraints)
        result = prob.solve(solver=cvx.MOSEK)

        return schedule.value, power, len(where_violation)


    def run(self,
            county,
            rate_energy_peak,
            rate_energy_partpeak,
            rate_energy_offpeak,
            rate_demand_peak,
            rate_demand_partpeak,
            rate_demand_overall
        ):
        self.county = county
        self.rate_energy_peak = rate_energy_peak
        self.rate_energy_partpeak = rate_energy_partpeak
        self.rate_energy_offpeak = rate_energy_offpeak
        self.rate_demand_peak = rate_demand_peak
        self.rate_demand_partpeak = rate_demand_partpeak
        self.rate_demand_overall = rate_demand_overall

        num_runs = 4
        peak_inds = np.arange(int(12*4), int(18*4))
        partpeak_inds = np.concatenate((np.arange(int(8.5*4), int(12*4)), np.arange(int(18*4), int(21.5*4))))
        energy_prices = np.concatenate((np.repeat(rate_energy_offpeak, int(8.5*4)), np.repeat(rate_energy_partpeak, int(3.5*4)),
                            np.repeat(rate_energy_peak, int(6*4)), np.repeat(rate_energy_partpeak, int(3.5*4)),
                            np.repeat(rate_energy_offpeak, int(2.5*4))))

        # example: county = 'Santa Clara'
        baseline_profiles = np.zeros((96, num_runs))
        controlled_profiles = np.zeros((96, num_runs))
        saved_indices = np.zeros((200, num_runs))
        list_violations = []
        for i in range(num_runs):
            print('On run: ', i)
            df, df_intervals, chosen_sessions = self.new_df_and_sessions(county, 200) #this first!
            saved_indices[:, i] = chosen_sessions
            power, arrival_inds, departure_inds, energies = self.uncontrolled_load(200, chosen_sessions, df, df_intervals, 6.6)
            schedule, power, violations = self.controlled_load(200, 6.6, arrival_inds, departure_inds, power, energies, energy_prices,
                            rate_demand_peak, rate_demand_partpeak, rate_demand_overall, peak_inds, partpeak_inds)

            baseline_profiles[:, i] = np.sum(power, axis=1)
            controlled_profiles[:, i] = np.sum(schedule, axis=1)
            list_violations.append(violations)

        #np.save(sca_dir + "baseline_profiles_" + county.replace(' ', '_') + "_500.npy", baseline_profiles)
        #np.save(sca_dir + "controlled_profiles_" + county.replace(' ', '_') + "_500.npy", controlled_profiles)

        return baseline_profiles, controlled_profiles
        #smf = SmartChargingFitting(baseline_profiles, controlled_profiles)
        #smf.run()

    def uploadToPostgres(self, baseline_profiles, controlled_profiles):
        # upload result to postgres
        upload_to_postgres_client = UploadToPostgres(
            self.county,
            self.rate_energy_peak,
            self.rate_energy_partpeak,
            self.rate_energy_offpeak,
            self.rate_demand_peak,
            self.rate_demand_partpeak,
            self.rate_demand_overall
        )
        upload_to_postgres_client.run(baseline_profiles, controlled_profiles)
        print('Upload to Postgres succeeded.')

    def demo_run(
            self,
            county,
            rate_energy_peak,
            rate_energy_partpeak,
            rate_energy_offpeak,
            rate_demand_peak,
            rate_demand_partpeak,
            rate_demand_overall
        ):
        self.county = county
        self.rate_energy_peak = rate_energy_peak
        self.rate_energy_partpeak = rate_energy_partpeak
        self.rate_energy_offpeak = rate_energy_offpeak
        self.rate_demand_peak = rate_demand_peak
        self.rate_demand_partpeak = rate_demand_partpeak
        self.rate_demand_overall = rate_demand_overall
        baseline_profiles = np.load("baseline_profiles_Santa_Clara_500.npy")
        controlled_profiles = np.load("controlled_profiles_Santa_Clara_500.npy")
        self.uploadToPostgres(baseline_profiles, controlled_profiles)

if __name__ == "__main__":
    # test
    sca = SmartChargingAlgorithm('script.chargepoint.data')
    baseline_profiles, controlled_profiles = sca.run('Santa Clara', 0.16997, 0.12236, 0.09082, 21.23, 5.85, 19.10)
    sca.uploadToPostgres(baseline_profiles, controlled_profiles)

    tz_NY = pytz.timezone('America/New_York')
    datetime_NY = datetime.now(tz_NY)
    print("us-east-1 time:", datetime_NY.strftime("%H:%M:%S"))
