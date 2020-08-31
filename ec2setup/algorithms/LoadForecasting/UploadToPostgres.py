import boto3
import json
import psycopg2


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
        with open('postgres_info.json') as json_file:
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
        publicl2_percent
    ):

        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        cur = conn.cursor()

        # create table on Postgres
        # cur.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id serial PRIMARY KEY, aggregation_level varchar, num_evs INTEGER," + \
        #     " choice varchar, fast_percent numeric, work_percent numeric, res_percent numeric, l1_percent numeric, public_l2_percent numeric, residential_l1_load varchar, residential_l2_load varchar, residential_mud_load varchar," + \
        #     " work_load varchar, fast_load varchar, public_l2_load varchar, total_load varchar);")

        # cur.execute("CREATE TABLE IF NOT EXISTS " + self.config_table_name + " (id serial PRIMARY KEY, config_name varchar, aggregation_level varchar, num_evs INTEGER," + \
        #     " choice varchar, fast_percent numeric, work_percent numeric, res_percent numeric, l1_percent numeric, public_l2_percent numeric);")

        cur.execute("INSERT INTO " + self.config_table_name + \
            " (config_name, aggregation_level, num_evs, choice," + \
            " fast_percent, work_percent, res_percent, l1_percent, public_l2_percent)" + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                str(config_name), str(aggregation_level), str(int(num_evs)), str(county_choice), str(fast_percent), \
                    str(work_percent), str(res_percent), str(l1_percent), str(publicl2_percent)
            )
        )

        conn.commit()
        cur.execute("SELECT id FROM "+self.config_table_name + " ORDER BY id DESC LIMIT 1")
        config_id = cur.fetchone()

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
        print(time_point_len)

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
                str(config_id),
                json.dumps(residential_l1_load_list), json.dumps(residential_l2_load_list),
                json.dumps(residential_mud_load_list), json.dumps(fast_load_list),
                json.dumps(work_load_list), json.dumps(public_l2_load_list), json.dumps(total_load_list)
            )
        )

        print('Insertion finished...')
        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()