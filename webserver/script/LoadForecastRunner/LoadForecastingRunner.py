from evloadmodel import EVLoadModel
from configurations_script import FinalReport
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
from UploadToPostgres import *


total_num_evs = 5e6
aggregation_level = 'county'
county = 'Santa Clara'

res_percent=0.75
fast_percent=0.05
publicl2_percent=0.05
work_percent=0.15

rent_percent=0.1
l1_percent=0.2

res_l2_smooth=True

week_day=True

res_daily_use=0.8
work_daily_use=0.8
fast_daily_use=0.33
publicl2_daily_use=0.33

mixed_batteries=None

timer_control=None
work_control='minpeak'


config = FinalReport(total_num_evs=total_num_evs, aggregation_level=aggregation_level, county=county,
                     res_percent=res_percent, fast_percent=fast_percent, publicl2_percent=publicl2_percent, work_percent=work_percent,
                     rent_percent=rent_percent, l1_percent=l1_percent, res_l2_smooth=res_l2_smooth, week_day=week_day,
                     res_daily_use=res_daily_use, work_daily_use=work_daily_use, fast_daily_use=fast_daily_use, publicl2_daily_use=publicl2_daily_use,
                     mixed_batteries=mixed_batteries, time_steps=96)
config.control_folder_path = 'Control_Objects/AllCounties_250cars_noagg_tuned'
config.sample_fast=True

name = 'demo2'

model = EVLoadModel(config)
model.calculate_basic_load(verbose=False)

total = np.zeros((np.shape(model.load_segments['Residential L1']['Load'])[0], 7))
total[:, 0] = model.load_segments['Residential L1']['Load']
total[:, 1] = model.load_segments['Residential L2']['Load']
total[:, 2] = model.load_segments['Residential MUD']['Load']
total[:, 3] = model.load_segments['Work']['Load']
total[:, 4] = model.load_segments['Fast']['Load'][np.arange(0, 1440, 15)]
total[:, 5] = model.load_segments['Public L2']['Load']
total[:, 6] = np.sum(total, axis=1)
total_df = pd.DataFrame(data=total, columns=['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast', 'Public L2', 'Total'])

labels = ['Residential L1', 'Residential L2', 'MUD L2', 'Workplace L2', 'Public L2', 'Public DCFC']
# model.plot_labeled_load(other_labels=labels, set_ylim=6000, force_mw=True, save_str=None)
parent_path = Path(__file__).parent.absolute()
path = parent_path.parent

pd.DataFrame(model.sampled_loads_dict).to_csv(str(path)+'/CostBenefitAnalysis/cba_tool/EV_Loads/load_profiles/demo2.csv')

model.apply_control(control_rule=work_control, segment='Work')
savestr = 'work_control_'+str(work_control)
# model.plot_labeled_load(model.controlled_segmented_load, other_labels=labels, set_ylim=6000, force_mw=True, save_str=None)
#pd.DataFrame(model.sampled_controlled_loads_dict).to_csv('s3://script.forecast.inputsoutputs/Control_Paper_Scenarios/'+name+'_controlled_load_'+savestr+'.csv')

#upload_to_postgres_client = UploadToPostgres(
#     total[:, 0],
#     total[:, 1],
#     total[:, 2],
#     total[:, 3],
#     total[:, 4],
#     total[:, 5],
#     total[:, 6],
# )
# upload_to_postgres_client.run(
#     'profile-1',
#     aggregation_level,
#     total_num_evs,
#     county,
#     fast_percent,
#     work_percent,
#     res_percent,
#     l1_percent,
#     publicl2_percent
# )
# print('Upload to Postgres succeeded.')