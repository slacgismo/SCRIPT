import numpy as np
import pickle
import pandas as pd
import boto3



class FinalReport(object):
    """Simple case with residential, MUD, workplace, public L2, public fast charging."""
    def __init__(self, total_num_evs, aggregation_level='state', county=None, res_percent=0.5,
                 fast_percent=0.18, publicl2_percent=0.02,
                 work_percent=0.3, rent_percent=None,
                 l1_percent=0, res_l2_smooth=False, week_day=True,
                 res_daily_use=1.0, work_daily_use=1.0, fast_daily_use=0.3, publicl2_daily_use=1.0, even_spread_geo_percent=0.0, mixed_batteries=None):

        if mixed_batteries is None:
            self.mixed_distributions = False
        else:
            self.mixed_distributions = True
            self.mixed_distribution_proportions = mixed_batteries

        self.sample_fast = False
        self.week_day = week_day
        self.gmm_bucket = 'script.chargepoint.data'   # GET ORIGINAL CODE TO GENERATE GMM
        self.s3client = boto3.client('s3') 
        self.gmm_folder_path = 'Up_to_date_Combined_Cleaned/All_Together/Years/GMMs/'  # WILL HAVE TO CREATE THIS FOLDER PATH

        self.joint_gmms = True        

        self.control_bucket = 'script.forecast.inputsoutputs'  # NEED TO CREATE THIS FOLDER
        self.control_folder_path = 'Control_Objects/AllCounties_250cars_10agg'  # THESE ARE THE MAPPING FUNCTIONS -> GET CODE

        self.aggregation_level = aggregation_level
        if self.aggregation_level == 'state':
            self.num_ev_owners = int(total_num_evs)
        elif self.aggregation_level == 'county':
            if county is None:
                print('Error! County chosen as aggregation level but no county given.')
            else:
                geo_distribution = pd.read_csv(
                    's3://script.forecast.inputsoutputs/new_distribution_of_lightduty_evs_by_county.csv')  # IS THIS FROM CP DATA? -> GET CODE (OR FILE)
                geo_distribution['Fraction'] = geo_distribution['EVs'].values / geo_distribution['EVs'].sum()
                county_index = geo_distribution[geo_distribution['County'] == county].index[0]
                if even_spread_geo_percent > 0:
                    county_data = pd.read_csv('s3://script.forecast.inputsoutputs/county_data_simplyanalytics.csv')  # SHOULD WE GENERATE THIS OR USE IT AS IT IS
                    pop = county_data.loc[
                        county_data[county_data['Name'] == county + ' County, CA'].index, '# Population, 2019'].values[0]
                    pop_fraction = pop/(county_data['# Population, 2019'].sum())
                else:
                    pop_fraction = 0
                num_evs = int((geo_distribution.loc[county_index, 'Fraction'] * (
                            1 - even_spread_geo_percent) + pop_fraction * even_spread_geo_percent) * total_num_evs)
                self.num_ev_owners = num_evs
        self.num_res = int(res_daily_use * res_percent * self.num_ev_owners)
        self.num_fast = int(fast_daily_use * fast_percent * self.num_ev_owners)
        self.num_publicl2 = int(publicl2_daily_use * publicl2_percent * self.num_ev_owners)
        self.num_work = int(work_daily_use * work_percent * self.num_ev_owners)

        if rent_percent is None:
            county_data = pd.read_csv('s3://script.forecast.inputsoutputs/county_data_simplyanalytics.csv')  # SHOULD WE GENERATE THIS OR USE IT AS IT IS
            if self.aggregation_level == 'state':
                rent_percent = county_data['% Housing, Renter Occupied, 2019'].mean() / 100.0
            elif self.aggregation_level == 'county':
                county_index2 = np.where(county_data['Name'] == county + ' County, CA')[0][0]
                rent_percent = county_data.loc[county_index2, '% Housing, Renter Occupied, 2019'] / 100.0
        self.num_mud = int(rent_percent * self.num_res)
        self.num_res_l1 = int(l1_percent * (self.num_res - self.num_mud))
        self.num_res_l2 = int(self.num_res - self.num_mud - self.num_res_l1)

        self.time_step = 0.25
        self.num_time_steps = 96
        self.time_steps_per_hour = 4
        self.fast_time_steps_per_hour = 60
        self.fast_num_time_steps = int(60 * 24)

        self.categories_dict = {'Segment': ['Residential L1', 'Residential L2', 'Residential MUD', 'Work',
                                            'Public L2', 'Fast'],
                                'Label': ['Residential L1', 'Residential L2', 'Residential MUD', 'Workplace',
                                          'Public L2', 'Fast'],
                                'Vehicles': [self.num_res_l1, self.num_res_l2, self.num_mud, self.num_work,
                                             self.num_publicl2, self.num_fast],
                                'GMM Sub Path': ['sessions2019_home_slow_smoothl1_weekday_allbatt_se_5_gmm.p',
                                                 'sessions2019_home_slow_weekday_allbatt_se_5_gmm.p',
                                                 'sessions2019_mud_slow_weekday_allbatt_se_6_gmm.p',
                                                 'sessions2019_work_slow_weekday_allbatt_se_5_gmm.p',
                                                 'sessions2019_other_slow_weekday_allbatt_se_6_gmm.p',
                                                 'sessions2019_other_fast_weekday_allbatt_se_4_gmm.p'],
                                'Rate': [1.4, 6.6, 6.6, 6.6, 6.6, 150.0],
                                'Energy Clip': [40, 75, 75, 75, 75, 75],
                                'Num Time Steps': [self.num_time_steps, self.num_time_steps, self.num_time_steps,
                                                   self.num_time_steps, self.num_time_steps, self.fast_num_time_steps],
                                'Time Steps Per Hour': [self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.time_steps_per_hour,
                                                        self.time_steps_per_hour, self.fast_time_steps_per_hour],
                                'Start Time Scaler': [(1/(60*15)), (1/(60*15)), (1/(60*15)), (1/(60*15)),
                                                      (1/(60*15)), (1/60)]}

        if not self.week_day:
            self.categories_dict['GMM Sub Path'] = ['sessions2019_home_slow_smoothl1_weekend_allbatt_se_6_gmm.p',
                                                    'sessions2019_home_slow_weekend_allbatt_se_6_gmm.p',
                                                    'sessions2019_mud_slow_weekend_allbatt_se_8_gmm.p',
                                                    'sessions2019_work_slow_weekend_allbatt_se_4_gmm.p',
                                                    'sessions2019_other_slow_weekend_allbatt_se_6_gmm.p',
                                                    'sessions2019_other_fast_weekend_allbatt_se_5_gmm.p'] # GENERATE THESE FILES FOR NEW DATA UPLOADED

        if res_l2_smooth:
            self.categories_dict['GMM Sub Path'][1] = self.categories_dict['GMM Sub Path'][0]

