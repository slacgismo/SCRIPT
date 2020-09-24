from script.LoadForecasting.EvLoadModel import EVLoadModel
from script.LoadForecasting.configurations_script import FinalReport
import numpy as np
import pandas as pd
from script.LoadForecasting.UploadToPostgres import *

def lf_runner(
        total_num_evs,
        aggregation_level,
        county,
        fast_percent,
        work_percent,
        res_percent,
        l1_percent,
        publicl2_percent,
        res_daily_use,
        work_daily_use,
        fast_daily_use,
        rent_percent,
        res_l2_smooth,
        week_day,
        publicl2_daily_use,
        mixed_batteries,
        timer_control,
        work_control,
        config_name,
    ):
    
    config = FinalReport(total_num_evs=total_num_evs, aggregation_level=aggregation_level, county=county,
                         res_percent=res_percent, fast_percent=fast_percent, publicl2_percent=publicl2_percent, work_percent=work_percent,
                         rent_percent=rent_percent, l1_percent=l1_percent, res_l2_smooth=res_l2_smooth, week_day=week_day,
                         res_daily_use=res_daily_use, work_daily_use=work_daily_use, fast_daily_use=fast_daily_use, publicl2_daily_use=publicl2_daily_use,
                         mixed_batteries=mixed_batteries, time_steps=96)
    config.control_folder_path = 'Control_Objects/AllCounties_250cars_noagg_tuned'
    config.sample_fast=True

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

    # pd.DataFrame(model.sampled_loads_dict).to_csv('s3://script.forecast.inputsoutputs/Control_Paper_Scenarios/'+name+'_uncontrolled_load.csv')

    model.apply_control(control_rule=work_control, segment='Work')
    savestr = 'work_control_'+str(work_control)
    # pd.DataFrame(model.sampled_controlled_loads_dict).to_csv('s3://script.forecast.inputsoutputs/Control_Paper_Scenarios/'+name+'_controlled_load_'+savestr+'.csv')

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
        config_name,
        aggregation_level,
        total_num_evs,
        county,
        fast_percent,
        work_percent,
        res_percent,
        l1_percent,
        publicl2_percent
    )
    print('Upload to Postgres succeeded.')
