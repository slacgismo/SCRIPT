from EVLoadModel import EVLoadModel
from configurations import OngoingConfig
import numpy as np
import scipy as sp
import pandas as pd
import matplotlib.pyplot as plt
import s3fs
import boto3
import pickle
import pytz
from datetime import datetime
from UploadToPostgres import *

##################
# Make these inputs
aggregation_level = 'county'  # Can also be 'state' or 'zip'
num_evs = 1e6
county_choice = 'Santa Clara'
fast_percent = 0.1
work_percent = 0.2
res_percent = 0.7
l1_percent = 0.5
publicl2_percent = 0.0
##################
res_daily_use = 1.0
work_daily_use = 1.0
fast_daily_use = 0.5
rent_percent = 0.4

fast_charge_rate = 350.0 # kW
chosen_fast_distribution = 'fast_nonwp_weekday'  # default is 'Latest_Model/fast_whitespace_workingpeople'
start_time_scaler = 1.0 # matched to this ^ distribution, as some were fit to different units
energy_clip = 100  # max battery size to allow drawing from the energy distributions

# Create and Edit Configuration
config = OngoingConfig(num_evs, aggregation_level=aggregation_level, county=county_choice, fast_percent=fast_percent, 
                               work_percent=work_percent, res_percent=res_percent, l1_percent=l1_percent, publicl2_percent=publicl2_percent,
                               res_daily_use=res_daily_use, work_daily_use=work_daily_use, fast_daily_use=fast_daily_use, rent_percent=rent_percent)
config.categories_dict['Rate'][5] = fast_charge_rate
config.categories_dict['GMM Sub Path'][5] = chosen_fast_distribution
config.categories_dict['Energy Clip'][5] = energy_clip
config.categories_dict['Start Time Scaler'][5] = start_time_scaler

# Model
model = EVLoadModel(config)
model.calculate_basic_load(verbose=False)

# save outcome
total = np.zeros((np.shape(model.load_segments['Residential L1']['Load'])[0], 7))
total[:, 0] = model.load_segments['Residential L1']['Load']
total[:, 1] = model.load_segments['Residential L2']['Load']
total[:, 2] = model.load_segments['Residential MUD']['Load']
total[:, 3] = model.load_segments['Work']['Load']
total[:, 4] = model.load_segments['Fast']['Load'][np.arange(0, 1440, 15)]
total[:, 5] = model.load_segments['Public L2']['Load']
total[:, 6] = np.sum(total, axis=1)
total_df = pd.DataFrame(data=total, columns=['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast', 'Public L2', 'Total'])

# Plot Outcome
def stacked_figure(xrange, part1, part2, part3, part4, part5, part6, full, legend_labels=['Res L1','Res L2','WP','Fast','Public','Fleet', 'Total'], num_parts=6, savestr=None, title=None):
    
    plt.figure(figsize=(8,5))
    if num_parts > 0:
        plt.plot(xrange, part1, 'C0')
        plt.fill_between(xrange, 0, part1, color='C0', alpha=0.5)
    if num_parts > 1:
        plt.plot(xrange, part1+part2, 'C1')
        plt.fill_between(xrange, part1, part1+part2, color='C1', alpha=0.5)
    if num_parts > 2:
        plt.plot(xrange, part1+part2+part3, 'C2')
        plt.fill_between(xrange, part1+part2, part1+part2+part3, color='C2', alpha=0.5)
    if num_parts > 3:
        plt.plot(xrange, part1+part2+part3+part4, 'C3')
        plt.fill_between(xrange, part1+part2+part3, part1+part2+part3+part4, color='C3', alpha=0.5)
    if num_parts > 4:
        plt.plot(xrange, part1+part2+part3+part4+part5, 'C4')
        plt.fill_between(xrange, part1+part2+part3+part4, part1+part2+part3+part4+part5, color='C4', alpha=0.5)
    if num_parts > 5:
        plt.plot(xrange, part1+part2+part3+part4+part5+part6, 'C5')
        plt.fill_between(xrange, part1+part2+part3+part4+part5, part1+part2+part3+part4+part5+part6, color='C5', alpha=0.5)
    plt.plot(xrange, full, 'k')
        
    plt.xlabel('Hour of day')
    plt.ylabel('kW')
    plt.xlim([0, 23.75])
    plt.ylim([0, 1.1*np.max(total[:, 6])])
    plt.title(title)
    plt.legend(labels=legend_labels)
    plt.tight_layout()
    
    if savestr is not None:
        plt.savefig(savestr, bbox_inches='tight')
    
    plt.show()
    
    return plt

titlestr = 'Example Run'
plot_save_str = None#'../sample_plot.png'
labs = ['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast', 'Public L2', 'Total']
plt = stacked_figure(0.25*np.arange(0, 96), total[:, 0], total[:, 1], total[:, 2], total[:, 3], total[:, 4], total[:, 5], total[:, 6], legend_labels=labs, savestr=plot_save_str, title=titlestr)

# upload result to postgres 
upload_to_postgres_client = UploadToPostgres(
    total[:, 0],
    total[:, 1],
    total[:, 2],
    total[:, 3],
    total[:, 4],
    total[:, 5],
    total[:, 6],
)
upload_to_postgres_client.run(
    'profile-1',
    aggregation_level,
    num_evs,
    county_choice,
    fast_percent,
    work_percent,
    res_percent,
    l1_percent,
    publicl2_percent
)
print('Upload to Postgres succeeded.')