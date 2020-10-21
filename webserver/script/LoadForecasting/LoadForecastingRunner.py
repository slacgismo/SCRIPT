from script.LoadForecasting.evloadmodel import EVLoadModel
from script.LoadForecasting.configurations import FinalReport
import numpy as np
import pandas as pd
from script.LoadForecasting.UploadToPostgres import *
import logging
from pathlib import Path


logger = logging.getLogger(__name__)

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

    # below values are temp, will be updated on the next PR with updated alg files
    battery_dict = {'smallbatt': 0, 'allbatt':0.7, 'bigbatt':0.3}
    even_spread_geo_percent = 0

    config = FinalReport(total_num_evs=total_num_evs, aggregation_level='county', county=county,
                        res_percent=res_percent, fast_percent=fast_percent, publicl2_percent=publicl2_percent, work_percent=work_percent, rent_percent=rent_percent,
                        l1_percent=l1_percent, res_l2_smooth=False, week_day=week_day,
                        res_daily_use=res_daily_use, work_daily_use=work_daily_use, fast_daily_use=fast_daily_use, publicl2_daily_use=publicl2_daily_use,
                        even_spread_geo_percent=even_spread_geo_percent, mixed_batteries=battery_dict)
    model = EVLoadModel(config)
    model.calculate_basic_load(verbose=False)

    # uncontrolled data prep before db
    # 1440 rows -> 96 rows for better plotting in the fron end
    total = np.zeros((np.shape(model.load_segments['Residential L1']['Load'])[0], 7))
    total[:, 0] = model.load_segments['Residential L1']['Load']
    total[:, 1] = model.load_segments['Residential L2']['Load']
    total[:, 2] = model.load_segments['Residential MUD']['Load']
    total[:, 3] = model.load_segments['Work']['Load']
    total[:, 4] = model.load_segments['Fast']['Load'][np.arange(0, 96, 1)]
    total[:, 5] = model.load_segments['Public L2']['Load']
    total[:, 6] = np.sum(total, axis=1)
    total_df = pd.DataFrame(data=total, columns=['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast', 'Public L2', 'Total'])

    # controlled data prep before db
    # 1440 rows -> 96 rows for better plotting in the fron end
    model.apply_control(control_rule=work_control, segment='Work')
    total_controlled = np.zeros((np.shape(model.controlled_load_segments_dict['Residential L1']['Load'])[0], 7))
    total_controlled[:, 0] = model.controlled_load_segments_dict['Residential L1']['Load']
    total_controlled[:, 1] = model.controlled_load_segments_dict['Residential L2']['Load']
    total_controlled[:, 2] = model.controlled_load_segments_dict['Residential MUD']['Load']
    total_controlled[:, 3] = model.controlled_load_segments_dict['Work']['Load']
    total_controlled[:, 4] = model.controlled_load_segments_dict['Fast']['Load'][np.arange(0, 96, 1)]
    total_controlled[:, 5] = model.controlled_load_segments_dict['Public L2']['Load']
    total_controlled[:, 6] = np.sum(total_controlled, axis=1)
    total_controlled_df = pd.DataFrame(data=total_controlled, columns=['Residential L1', 'Residential L2', 'Residential MUD', 'Work', 'Fast', 'Public L2', 'Total'])

    # inputs to the cba tool
    path = Path(__file__).parent.resolve()
    parent_path = path.parent
    pd.DataFrame(model.sampled_loads_dict).to_csv(str(parent_path)+'/costbenefitanalysis/preprocessing_loadprofiles/inputs/weekdays/BaseCase_2025_weekday_' + county + '_county_uncontrolled_load.csv')
    pd.DataFrame(model.sampled_controlled_loads_dict).to_csv(str(parent_path)+'/costbenefitanalysis/preprocessing_loadprofiles/inputs/BaseCase_2025_weekday_' + county + '_county_controlled_load.csv')

    upload_to_postgres_client_uncontrolled = UploadToPostgres(
        total[:, 0],
        total[:, 1],
        total[:, 2],
        total[:, 3],
        total[:, 4],
        total[:, 5],
        total[:, 6],
        total_controlled[:, 0],
        total_controlled[:, 1],
        total_controlled[:, 2],
        total_controlled[:, 3],
        total_controlled[:, 4],
        total_controlled[:, 5],
        total_controlled[:, 6],
    )

    upload_to_postgres_client_uncontrolled.run(
        config_name,
        aggregation_level,
        total_num_evs,
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
        work_control
    )

    logger.info('Upload to Postgres for Load Forecasting succeeded.')
