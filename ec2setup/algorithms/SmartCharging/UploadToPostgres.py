import boto3
import json
import psycopg2


class UploadToPostgres():
    def __init__(
        self,
        county,
        rate_energy_peak,
        rate_energy_partpeak,
        rate_energy_offpeak,
        rate_demand_peak,
        rate_demand_partpeak,
        rate_demand_overall
    ):
        with open('postgres_info.json') as json_file:
            postgres_info = json.load(json_file)
        
        self.db_host = postgres_info['DB_HOST']
        self.table_name = "script_config_load_controller"
        self.postgres_db = postgres_info['POSTGRES_DB']
        self.postgres_user = postgres_info['POSTGRES_USER']
        self.postgres_password = postgres_info['POSTGRES_PASSWORD']
        self.county = county
        self.rate_energy_peak = rate_energy_peak
        self.rate_energy_partpeak = rate_energy_partpeak
        self.rate_energy_offpeak = rate_energy_offpeak
        self.rate_demand_peak = rate_demand_peak
        self.rate_demand_partpeak = rate_demand_partpeak
        self.rate_demand_overall = rate_demand_overall
        self.total_number_of_session = 0
        self.total_energy = 0
        self.num_of_run = 4

    def run(self, baseline_profiles, controlled_profiles):
        # update self.total_number_of_session
        self.total_number_of_session = len(baseline_profiles)

        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        cur = conn.cursor()


        # create table on Postgres
        # cur.execute("CREATE TABLE IF NOT EXISTS script_county" + " (id serial PRIMARY KEY, name varchar, total_energy float, total_session float," + \
        #     " rate_energy_peak varchar);")

        # create table on Postgres
        # cur.execute("CREATE TABLE IF NOT EXISTS " + self.table_name + " (id serial PRIMARY KEY, county varchar, rate_energy_peak varchar, rate_energy_partpeak varchar," + \
        #     " rate_energy_offpeak varchar, rate_demand_peak varchar, rate_demand_partpeak varchar, rate_demand_overall varchar, uncontrolled_load varchar, controlled_load varchar);")

        # upload data into Postgres
        baseline_profiles_list = []
        controlled_profiles_list = []

        start_hour = 0
        start_minute = 0

        lines = len(baseline_profiles / 4)
        for line in range(lines):
            hour_str = str((start_hour + line % 4)% 24)
            minute = 15 * (line % 4)
            if minute is 0:
                minute_str = '00'
            else:
                minute_str = str(minute)

            self.total_energy += int(baseline_profiles[line][self.num_of_run - 1])
            baseline_profiles_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(baseline_profiles[line][self.num_of_run - 1])
                }
            )

            controlled_profiles_list.append(
                {
                    'time': hour_str + ':' + minute_str,
                    'load': str(controlled_profiles[line][self.num_of_run - 1])
                }
            )

        cur.execute("INSERT INTO script_county" + \
            " (name, total_energy, total_session, peak_energy)" + \
            " VALUES (%s, %s, %s, %s)",
            (
                self.county, self.total_energy, self.total_number_of_session, self.rate_energy_peak
            )
        )

        conn.commit()

        county = cur.execute("SELECT * FROM script_county " + \
            "WHERE name = \"" + self.county +"\";")

        cur.execute("INSERT INTO " + self.table_name + \
            " (county, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak," + \
            " rate_demand_peak, rate_demand_partpeak, rate_demand_overall)" + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s)",
            (
                county, self.rate_energy_peak, self.rate_energy_partpeak, self.rate_energy_offpeak,
                self.rate_demand_peak, self.rate_demand_partpeak, self.rate_demand_overall
            )
        )

        conn.commit()

        config = cur.execute("SELECT * FROM " + self.table_name + \
            " WHERE county = \"" + county + "\"" \
            " AND rate_energy_peak = " + self.rate_energy_peak + \
            " AND rate_energy_partpeak = " + self.rate_energy_partpeak + \
            " AND rate_energy_offpeak = " + self.rate_energy_offpeak + \
            " AND rate_demand_peak = " + self.rate_demand_peak + \
            " AND rate_demand_partpeak = " + self.rate_demand_partpeak + \
            " AND rate_demand_overall = " + self.rate_demand_overall + ";")

        cur.execute("INSERT INTO script_algorithm_load_controller" + \
            " (config, uncontrolled_load, controlled_load)" + \
            " VALUES (%s, %s, %s)",
            (
                config, json.dumps(baseline_profiles_list), json.dumps(controlled_profiles_list) 
            )
        )

        print('Insertion finished...')
        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()