import numpy as np
import pickle
import pandas as pd


class OngoingConfig(object):
    """Simple case with residential, workplace, and non-workplace fast charging."""
    def __init__(self, total_num_evs, aggregation_level='state', zip_code=None, county=None, res_percent=0.5,
                 fast_percent=0.18, publicl2_percent=0.01,
                 work_percent=0.3, rent_percent=None,
                 l1_percent=0, res_l2_smooth=True, even_spread_of_fast=0.1, week_day=True,
                 res_daily_use=1.0, work_daily_use=1.0, fast_daily_use=0.3, publicl2_daily_use=1.0):

        self.sample_fast = False
        self.week_day = week_day

        self.aggregation_level = aggregation_level
        if self.aggregation_level == 'state':
            self.num_ev_owners = int(total_num_evs)
            self.num_res = int(res_daily_use * res_percent * self.num_ev_owners)
            self.num_fast = int(fast_daily_use * fast_percent * self.num_ev_owners)
            self.num_publicl2 = int(publicl2_daily_use * publicl2_percent * self.num_ev_owners)
            self.num_work = int(work_daily_use * work_percent * self.num_ev_owners)
            if rent_percent is None:
                county_data = pd.read_csv('s3://script.forecast.inputsoutputs/county_data_simplyanalytics.csv')
                rent_percent = county_data['% Housing, Renter Occupied, 2019'].mean() / 100.0

        if self.aggregation_level == 'county':
            if county is None:
                print('Error! County chosen as aggregation level but no county given.')
            else:
                geo_distribution = pd.read_csv('s3://script.forecast.inputsoutputs/distribution_of_lightduty_evs_by_county.csv')
                geo_distribution['Fraction'] = geo_distribution['EVs'].values / geo_distribution['EVs'].sum()
                county_index = geo_distribution[geo_distribution['County']==county].index[0]
                num_evs = int(geo_distribution.loc[county_index, 'Fraction'] * total_num_evs)
                self.num_ev_owners = num_evs
                self.num_res = int(res_daily_use * res_percent * self.num_ev_owners)
                self.num_fast = int(fast_daily_use * fast_percent * self.num_ev_owners)
                self.num_publicl2 = int(publicl2_daily_use * publicl2_percent * self.num_ev_owners)
                self.num_work = int(work_daily_use * work_percent * self.num_ev_owners)

                if rent_percent is None:
                    county_data = pd.read_csv('s3://script.forecast.inputsoutputs/county_data_simplyanalytics.csv')
                    county_index2 = np.where(county_data['Name'] == county + ' County, CA')[0][0]
                    rent_percent = county_data.loc[county_index2, '% Housing, Renter Occupied, 2019']/100.0

        if self.aggregation_level == 'zip':
            if zip_code is None:
                print('Error! Zip chosen as aggregation level but no zip_code given.')
            else:
                # Home zip distribution
                zip_stats = pd.read_csv('s3://script.forecast.inputsoutputs/census_fittings.csv', index_col=0)
                num_zips = len(zip_stats)
                zip_stats = zip_stats[zip_stats['Zip Code'] == zip_code]
                gamma_scaler1 = total_num_evs / 489784.67  # see "Fitting to Correlations"
                self.num_ev_owners = 0
                if len(zip_stats) > 0:
                    self.num_ev_owners = 0
                    if zip_stats['Median Household Income'].values[0] > 0:
                        self.num_ev_owners = gamma_scaler1 * -81.96765355
                        self.num_ev_owners += gamma_scaler1 * 0.00468634 * zip_stats['Median Household Income'].values[0]

                self.num_res = int(res_daily_use * res_percent * self.num_ev_owners)
                base_fast = int(even_spread_of_fast * fast_percent * total_num_evs)
                self.base_num_fast = int(base_fast * (1/num_zips))
                self.num_fast = int(fast_daily_use * fast_percent * self.num_ev_owners * (1 - even_spread_of_fast)
                                    + self.base_num_fast)
                self.num_publicl2 = int(publicl2_daily_use * publicl2_percent * self.num_ev_owners)

                # Workplace zip
                gamma_scaler2 = total_num_evs / 34248.690  # See "Fitting to Correlations"
                self.num_wp_stations = 0
                if len(zip_stats) > 0:
                    if zip_stats['Number of Employees'].values[0] > 0:
                        self.num_wp_stations += gamma_scaler2 * (0.00426860 * zip_stats['Number of Employees'].values[0])
                    if zip_stats['Salary'].values[0] > 0:
                        self.num_wp_stations += gamma_scaler2 * (0.00100704 * zip_stats['Salary'].values[0])
                    if zip_stats['Establishments'].values[0] > 0:
                        self.num_wp_stations += gamma_scaler2 * (- 0.11240321 * zip_stats['Establishments'].values[0])
                    if self.num_wp_stations < 0:  # weird
                        self.num_wp_stations = 0

                self.num_work = int(work_daily_use * work_percent * self.num_wp_stations)

                if rent_percent is None:
                    try:
                        census = pd.read_csv('s3://script.forecast.inputsoutputs/CSV_Files/census_data_all_simplyanalytics.csv')
                        census_ind = np.where(census['FIPS'] == int(zip_code))[0][0]
                        rent_percent = census.loc[census_ind, '% Housing, Renter Occupied, 2018'] / 100.0
                    except:
                        rent_percent = 0

        self.time_step = 0.25
        self.num_time_steps = 96
        self.time_steps_per_hour = 4
        self.fast_time_steps_per_hour = 60
        self.fast_num_time_steps = int(60 * 24)

        self.num_mud = int(rent_percent * self.num_res)
        self.num_res_l1 = int(l1_percent * (self.num_res - self.num_mud))
        self.num_res_l2 = int(self.num_res - self.num_mud - self.num_res_l1)

        self.categories_dict = {'Segment': ['Residential L1', 'Residential L2', 'Residential MUD', 'Work',
                                            'Public L2', 'Fast'],
                                'Label': ['Residential L1', 'Residential L2', 'Residential MUD', 'Workplace',
                                          'Public L2', 'Fast'],
                                'Vehicles': [self.num_res_l1, self.num_res_l2, self.num_mud, self.num_work,
                                             self.num_publicl2, self.num_fast],
                                'GMM Sub Path': ['Latest_Model/res_smooth', 'Latest_Model/res', 'Latest_Model/mud',
                                                 'Latest_Model/wp', 'Latest_Model/publicl2',
                                                 'Latest_Model/fast_whitespace_workingpeople'],
                                'Rate': [1.4, 6.6, 6.6, 6.6, 6.6, 150.0],
                                'Energy Clip': [40, 75, 75, 75, 75, 75],
                                'Num Time Steps': [self.num_time_steps, self.num_time_steps, self.num_time_steps,
                                                   self.num_time_steps, self.num_time_steps, self.fast_num_time_steps],
                                'Time Steps Per Hour': [self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.fast_time_steps_per_hour],
                                'Start Time Scaler': [1.0, 1.0, 1.0, 1.0, 1.0, 60.0]}

        # Other fast gmm: /fast_nonwp_weekday, Latest_Model/weekend_fast_nonwp
        if not self.week_day:
            self.categories_dict['GMM Sub Path'] = ['Latest_Model/weekend_res_smooth', 'Latest_Model/weekend_res',
                                                    'Latest_Model/weekend_mud', 'Latest_Model/weekend_wp',
                                                    'Latest_Model/weekend_publicl2',
                                                    'Latest_Model/weekend_fast_whitespace_workingpeople']

        if res_l2_smooth:
            if self.week_day:
                self.categories_dict['GMM Sub Path'][1] = 'Latest_Model/res_smooth'
            else:
                self.categories_dict['GMM Sub Path'][1] = 'Latest_Model/weekend_res_smooth'

        self.gmm_folder_path = '../GMMs/'

        self.base_config = 'CAISO'
        self.base_config_scaling = 'pop_and_emp'
        self.base_load_scale_2030 = 1.13


class SimpleFast(object):
    """The simple fast configuration from before Sept 23. Simple case with residential, workplace, and
    non-workplace fast charging."""
    def __init__(self, zip_code, total_num_evs, res_percent=0.5, fast_percent=0.2, work_percent=0.3, rent_percent=None,
                 l1_percent=0, res_l2_smooth=True, even_spread_of_fast=0.1, week_day=True,
                 res_daily_use=1.0, work_daily_use=1.0, fast_daily_use=0.3):

        self.sample_fast = False
        self.week_day = week_day

        # Home zip distribution
        zip_stats = pd.read_csv('s3://script.forecast.inputsoutputs/census_fittings.csv', index_col=0)
        num_zips = len(zip_stats)
        zip_stats = zip_stats[zip_stats['Zip Code'] == zip_code]
        gamma_scaler1 = total_num_evs / 489784.67  # see "Fitting to Correlations"
        self.num_ev_owners = 0
        if len(zip_stats) > 0:
            self.num_ev_owners = 0
            if zip_stats['Median Household Income'].values[0] > 0:
                self.num_ev_owners = gamma_scaler1 * -81.96765355
                self.num_ev_owners += gamma_scaler1 * 0.00468634 * zip_stats['Median Household Income'].values[0]

        self.num_res = int(res_daily_use * res_percent * self.num_ev_owners)
        base_fast = int(even_spread_of_fast * fast_percent * total_num_evs)
        self.base_num_fast = int(base_fast * (1/num_zips))
        self.num_fast = int(fast_daily_use * fast_percent * self.num_ev_owners * (1 - even_spread_of_fast)
                            + self.base_num_fast)

        # Workplace zip
        gamma_scaler2 = total_num_evs / 34248.690  # See "Fitting to Correlations"
        self.num_wp_stations = 0
        if len(zip_stats) > 0:
            if zip_stats['Number of Employees'].values[0] > 0:
                self.num_wp_stations += gamma_scaler2 * (0.00426860 * zip_stats['Number of Employees'].values[0])
            if zip_stats['Salary'].values[0] > 0:
                self.num_wp_stations += gamma_scaler2 * (0.00100704 * zip_stats['Salary'].values[0])
            if zip_stats['Establishments'].values[0] > 0:
                self.num_wp_stations += gamma_scaler2 * (- 0.11240321 * zip_stats['Establishments'].values[0])
            if self.num_wp_stations < 0:  # weird
                self.num_wp_stations = 0

        self.num_work = int(work_daily_use * work_percent * self.num_wp_stations)

        if rent_percent is None:
            try:
                census = pd.read_csv('s3://script.forecast.inputsoutputs/CSV_Files/census_data_all_simplyanalytics.csv')
                census_ind = np.where(census['FIPS'] == int(zip_code))[0][0]
                rent_percent = census.loc[census_ind, '% Housing, Renter Occupied, 2018'] / 100.0
            except:
                rent_percent = 0

        self.time_step = 0.25
        self.num_time_steps = 96
        self.time_steps_per_hour = 4
        self.fast_time_steps_per_hour = 60
        self.fast_num_time_steps = int(60 * 24)

        self.num_mud = int(rent_percent * self.num_res)
        self.num_res_l1 = int(l1_percent * (self.num_res - self.num_mud))
        self.num_res_l2 = int(self.num_res - self.num_mud - self.num_res_l1)

        self.categories_dict = {'Segment': ['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast'],
                                'Label': ['Residential L1', 'Residential L2', 'Residential MUD', 'Workplace', 'Fast'],
                                'Vehicles': [self.num_res_l1, self.num_res_l2, self.num_mud, self.num_work,
                                             self.num_fast],
                                'GMM Sub Path': ['Latest_Model/res_smooth', 'Latest_Model/res', 'Latest_Model/mud',
                                                 'Latest_Model/cluster1', 'fast_nonwp_weekday'],
                                'Rate': [1.4, 6.6, 6.6, 6.6, 150.0],
                                'Energy Clip': [40, 75, 75, 75, 75],
                                'Num Time Steps': [self.num_time_steps, self.num_time_steps, self.num_time_steps,
                                                   self.num_time_steps, self.fast_num_time_steps],
                                'Time Steps Per Hour': [self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.fast_time_steps_per_hour]}

        if not self.week_day:
            self.categories_dict['GMM Sub Path'] = ['Latest_Model/weekend_res_smooth', 'Latest_Model/weekend_res',
                                                    'Latest_Model/weekend_mud', 'Latest_Model/weekend_wp',
                                                    'Latest_Model/weekend_fast_nonwp']

        if res_l2_smooth:
            if self.week_day:
                self.categories_dict['GMM Sub Path'][1] = 'Latest_Model/res_smooth'
            else:
                self.categories_dict['GMM Sub Path'][1] = 'Latest_Model/weekend_res_smooth'

        self.gmm_folder_path = '../GMMs/'

        self.base_config = 'CAISO'
        self.base_config_scaling = 'pop_and_emp'
        self.base_load_scale_2030 = 1.13



class InitialConfig(object):
    """Latest set of configurations for testing and development."""
    
    def __init__(self):
        
        self.mobility = False

        self.sample_fast = True

        self.time_step = 0.25
        self.num_time_steps = 96
        self.time_steps_per_hour = 4
        self.fast_time_steps_per_hour = 60
        self.fast_num_time_steps = int(60*24)

        self.base_config = 'CPUC'
        self.base_config_scaling = 'pop_and_emp'
        self.base_load_scale_2030 = 1.13

        self.week_day = True  # Else weekend/holiday

        self.num_ev = 5e6
        self.simple_proportions = {'l1': 0.4, 'l2': 0.1, 'wp': 0.25, 'fast': 0.15, 'public_l2': 0.05, 'fleet': 0.05}
        self.num_l1 = int(self.num_ev*self.simple_proportions['l1'])
        self.num_l2 = int(self.num_ev*self.simple_proportions['l2'])
        self.num_wp = int(self.num_ev*self.simple_proportions['wp'])
        self.num_fast = int(self.num_ev*self.simple_proportions['fast'])
        self.num_public = int(self.num_ev*self.simple_proportions['public_l2'])
        self.num_fleet = int(self.num_ev*self.simple_proportions['fleet'])
        
        self.l1_rate = 1.4
        self.l2_rate = 6.6
        self.wp_rate = 6.6
        self.fast_rate = 50.0
        self.fleet_rate = 6.6

        self.static_distribution_inputs = False
        self.simple_residential_l1 = True
        self.l1_start_centers = np.array([18, 12]) 
        self.l1_start_stds = np.array([2.5, 2.0])
        self.l1_start_quants = np.array([10000.0, 500.0]).astype(int)
        self.l1_energy_centers = np.array([12.0, 5.0])
        self.l1_energy_stds = np.array([4.0, 3.5])
        self.l1_energy_quants = np.array([10000, 10000]).astype(int)
        self.l1_energy_clip = 40

        self.simple_residential_l2 = True
        self.l2_start_centers = np.array([18, 20])
        self.l2_start_stds = np.array([2.5, 3.0])
        self.l2_start_quants = np.array([10000.0, 1000.0]).astype(int)
        self.l2_energy_centers = np.array([25.0, 10.0])
        self.l2_energy_stds = np.array([10.0, 5.0])
        self.l2_energy_quants = np.array([10000, 10000]).astype(int)
        self.l2_energy_clip = 75
        
        self.simple_workplace = True
        self.wp_energy_clip = 75
        self.wp_zip_clustering = True
        self.wp_num_zip_clusters = 3
        self.wp_zip_clustering_saved = False

        self.fast_energy_clip = 75
        self.simple_public = True

        self.public_energy_clip = 75

        self.fleet_energy_clip = 75
        self.simple_fleet = True

        if self.static_distribution_inputs is False:
            self.l1_start_distribution = pickle.load(open("GMMS/l1_arrival_dist.p", "rb"))
            self.l1_energy_distribution = pickle.load(open("GMMS/l1_energy_dist.p", "rb"))

            self.l2_start_distribution = pickle.load(open("GMMS/l2_arrival_dist.p", "rb"))
            self.l2_energy_distribution = pickle.load(open("GMMS/l2_energy_dist.p", "rb"))

            self.wp_start_distribution = pickle.load(open("GMMS/wp_arrival_dist.p", "rb"))
            self.wp_energy_distribution = pickle.load(open("GMMS/wp_energy_dist.p", "rb"))

            self.fast_start_distribution = pickle.load(open("GMMS/fast_public_arrival_dist.p", "rb"))
            self.fast_energy_distribution = pickle.load(open("GMMS/fast_public_energy_dist.p", "rb"))

            self.public_start_distribution = pickle.load(open("GMMS/public_arrival_dist.p", "rb"))
            self.public_energy_distribution = pickle.load(open("GMMS/public_energy_dist.p", "rb"))

            self.fleet_start_distribution = pickle.load(open("GMMS/fleet_arrival_dist.p", "rb"))
            self.fleet_energy_distribution = pickle.load(open("GMMS/fleet_energy_dist.p", "rb"))

    def redo_proportions(self):
        self.num_l1 = int(self.num_ev * self.simple_proportions['l1'])
        self.num_l2 = int(self.num_ev * self.simple_proportions['l2'])
        self.num_wp = int(self.num_ev * self.simple_proportions['wp'])
        self.num_fast = int(self.num_ev * self.simple_proportions['fast'])
        self.num_public = int(self.num_ev * self.simple_proportions['public_l2'])
        self.num_fleet = int(self.num_ev * self.simple_proportions['fleet'])


class PerZIPConfig(object):
    """Uses clustering results to build zip charging profile based on census figures. Note took out fleet."""

    def __init__(self, penetration_level, zip_code, population=None, employees=None, rent_percent=None,
                 public_wp_split=None, l1_percent=0,
                 fast_public_percent=0.3, fast_other_percent=0, res_comm_split=0.5,
                 census=None, category_equivalence=None):

        self.sample_fast = True
        self.week_day = True

        self.pen_model = 'Linear'

        if census is None:
            census = pd.read_csv('s3://script.forecast.inputsoutputs/CSV_Files/census_data_all_simplyanalytics.csv')
        census2 = census[['# Population, 2018', 'Median Household Income, 2018']].sort_values(
            by='Median Household Income, 2018', ascending=False)
        census2['Product'] = census2['# Population, 2018'] * census2['Median Household Income, 2018']
        census2 = census2[:-2]
        census_ind = np.where(census['FIPS'] == int(zip_code))[0][0]

        cluster_percents = None
        if sum(np.isnan(census2.loc[census_ind]).values) > 0:
            print('Nans here')
            rent_percent = 0
            cluster_percents = np.zeros((4, ))

        employee_inds = np.concatenate((np.concatenate((np.arange(24, 53, 2), np.array([53]))), np.arange(56, 78, 2)))
        if category_equivalence is None:
            category_equivalence = pd.read_csv('s3://script.forecast.inputsoutputs/category_equivalence.csv')
        count_df = census[census['FIPS'] == zip_code].reset_index(drop=True).loc[0, census.columns[employee_inds]]
        if cluster_percents is None:
            if np.max(count_df.values) > 0:
                cluster_counts, cluster_percents = num_per_cluster(count_df, category_equivalence)
            else:
                cluster_percents = np.zeros((4, ))
        if public_wp_split is None:
            public_wp_split = {1: cluster_percents[0], 2: cluster_percents[1],
                               3: cluster_percents[2], 4: cluster_percents[3]}

        if rent_percent is None:
            rent_percent = census.loc[census_ind, '% Housing, Renter Occupied, 2018'] / 100

        self.pen_coefficient = penetration_level * census2['# Population, 2018'].sum() / (census2['Product'].sum())
        self.census_product_df = census2

        self.time_step = 0.25
        self.num_time_steps = 96
        self.time_steps_per_hour = 4
        self.fast_time_steps_per_hour = 60
        self.fast_num_time_steps = int(60 * 24)
        if not np.isnan(census2.loc[census_ind, 'Product']):
            self.num_ev = int(self.pen_coefficient * census2.loc[census_ind, 'Product'])
        else:
            self.num_ev = 0
        self.num_res = int(res_comm_split*self.num_ev)
        self.num_comm = int((1-res_comm_split)*self.num_ev)

        # self.num_ev = int(penetration_level * (population + employees))
        # self.num_res = int(penetration_level * population * res_comm_split)
        # self.num_comm = self.num_ev - self.num_res

        self.num_mud = int(rent_percent * self.num_res * (1-fast_other_percent))
        self.num_single_home = int((1-rent_percent) * self.num_res * (1-fast_other_percent))
        self.num_res_l1 = int(l1_percent * self.num_single_home)
        self.num_res_l2 = int((1-l1_percent) * self.num_single_home )
        self.num_per_cluster = [int(public_wp_split[1] * self.num_comm * (1-fast_other_percent)),
                                int(public_wp_split[2] * self.num_comm * (1-fast_public_percent)),
                                int(public_wp_split[3] * self.num_comm * (1-fast_other_percent)),
                                int(public_wp_split[4] * self.num_comm * (1-fast_public_percent))]

        self.num_fast = int(fast_public_percent * (public_wp_split[2]+public_wp_split[4]) * self.num_comm +
                            fast_other_percent * (public_wp_split[1]+public_wp_split[3]) * self.num_comm +
                            fast_other_percent * self.num_res)

        self.res_l2_smooth = False

        self.categories_dict = {'Segment': ['Residential L1', 'Residential L2', 'Residential MUD', 'PublicWP_Cluster1',
                                            'PublicWP_Cluster2', 'PublicWP_Cluster3', 'PublicWP_Cluster4',
                                            'Fast'],
                                'Label': ['Residential L1', 'Residential L2', 'Residential MUD', 'Workplace', 'Public',
                                          'Workplace', 'Public', 'Fast'],
                                'Vehicles': [self.num_res_l1, self.num_res_l2, self.num_mud, self.num_per_cluster[0],
                                             self.num_per_cluster[1], self.num_per_cluster[2], self.num_per_cluster[3],
                                             self.num_fast],
                                'GMM Sub Path': ['res_smooth', 'res', 'mud', 'cluster1', 'cluster2', 'cluster3', 'cluster4',
                                                 'fast'],
                                'Rate': [1.4, 6.6, 6.6, 6.6, 6.6, 6.6, 6.6, 50.0],
                                'Energy Clip': [40, 75, 75, 75, 75, 75, 75, 75],
                                'Num Time Steps': [self.num_time_steps, self.num_time_steps, self.num_time_steps,
                                                   self.num_time_steps, self.num_time_steps, self.num_time_steps,
                                                   self.num_time_steps, self.fast_num_time_steps],
                                'Time Steps Per Hour': [self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.fast_time_steps_per_hour]}
        if self.res_l2_smooth:
            self.categories_dict['GMM Sub Path'][1] = 'res_smooth'

        self.gmm_folder_path = '../GMMs/Latest_Model/'

        self.base_config = 'CPUC'
        self.base_config_scaling = 'pop_and_emp'
        self.base_load_scale_2030 = 1.13


def num_per_cluster(count_df, category_equivalence):
    cluster_counts = np.zeros((np.max(category_equivalence['Cluster'].values),))
    for i in range(len(count_df)):
        key = count_df.index[i]
        cluster = category_equivalence[category_equivalence['Census Category'] == key]['Cluster'].values[0]
        cluster_counts[int(cluster - 1)] += count_df[i]

    cluster_percents = cluster_counts / np.sum(cluster_counts)
    return cluster_counts, cluster_percents
