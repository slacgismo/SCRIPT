import boto3
import json
import psycopg2
from django.conf import settings


class UploadToPostgres():
    def __init__(
        self,
        residential_l1_load,
        residential_l2_load,
        residential_mud_load,
        work_load,
        fast_load,
        public_l2_load,
        total_load
    ):

        with open(settings.BASE_DIR + '/postgres_info.json') as json_file:
            postgres_info = json.load(json_file)

        self.db_host = postgres_info['DB_HOST']
        self.table_name = "script_algorithm_ev_load_forecast"
        self.config_table_name = "script_config_ev_load_forecast"
        self.postgres_db = postgres_info['POSTGRES_DB']
        self.postgres_user = postgres_info['POSTGRES_USER']
        self.postgres_password = postgres_info['POSTGRES_PASSWORD']
        self.residential_l1_load = residential_l1_load
        self.residential_l2_load = residential_l2_load
        self.residential_mud_load = residential_mud_load
        self.fast_load = fast_load
        self.work_load = work_load
        self.public_l2_load = public_l2_load
        self.total_load = total_load

    def run(
        self,
        config_name,
        aggregation_level,
        num_evs,
        county_choice,
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

    ):

        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        cur = conn.cursor()

        cur.execute("INSERT INTO " + self.config_table_name + \
            " (config_name, aggregation_level, num_evs, choice," + \
            " fast_percent, work_percent, res_percent, l1_percent, public_l2_percent," + \
            " res_daily_use, work_daily_use, fast_daily_use, rent_percent, res_l2_smooth," + \
            " week_day, publicl2_daily_use, mixed_batteries, timer_control, work_control)" + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                str(config_name), str(aggregation_level), str(int(num_evs)), str(county_choice), str(fast_percent), \
                str(work_percent), str(res_percent), str(l1_percent), str(publicl2_percent), str(res_daily_use), \
                str(work_daily_use), str(fast_daily_use), str(rent_percent), str(res_l2_smooth), str(week_day), \
                str(publicl2_daily_use), str(mixed_batteries), str(timer_control), str(work_control)
            )
        )

        conn.commit()

        # upload data into Postgres
        residential_l1_load_list = []
        residential_l2_load_list = []
        residential_mud_load_list = []
        fast_load_list = []
        work_load_list = []
        public_l2_load_list = []
        total_load_list = []

        start_hour = 0
        start_minute = 0

        time_point_len = len(self.residential_l1_load)

        for i in range(time_point_len):
            hour_str = str((start_hour + i // 4) % 24)
            minute = 15 * (i % 4)
            if minute is 0:
                minute_str = '00'
            else:
                minute_str = str(minute)

            residential_l1_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.residential_l1_load[i], 2))
                }
            )

            residential_l2_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.residential_l2_load[i], 2))
                }
            )

            residential_mud_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.residential_mud_load[i], 2))
                }
            )

            fast_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.fast_load[i], 2))
                }
            )

            work_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.work_load[i], 2))
                }
            )

            public_l2_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.public_l2_load[i], 2))
                }
            )

            total_load_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(round(self.total_load[i], 2))
                }
            )

        cur.execute("INSERT INTO " + self.table_name + \
            " (config, residential_l1_load, residential_l2_load, residential_mud_load, fast_load," + \
            " work_load, public_l2_load, total_load)" + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
            (
                str(config_name),
                json.dumps(residential_l1_load_list), json.dumps(residential_l2_load_list),
                json.dumps(residential_mud_load_list), json.dumps(fast_load_list),
                json.dumps(work_load_list), json.dumps(public_l2_load_list), json.dumps(total_load_list)
            )
        )
        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()