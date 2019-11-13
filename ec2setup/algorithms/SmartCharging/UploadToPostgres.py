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
        self.table_name = "script_algorithm_load_controller"
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

    def run(self, baseline_profiles, controlled_profiles):
        conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        cur = conn.cursor()

        # create table on Postgres
        cur.execute("CREATE TABLE " + self.table_name + " (id serial PRIMARY KEY, county varchar, rate_energy_peak varchar, rate_energy_partpeak varchar," + \
            " rate_energy_offpeak varchar, rate_demand_peak varchar, rate_demand_partpeak varchar, rate_demand_overall varchar, uncontrolled_load varchar, controlled_load varchar);")

        # upload data into Postgres
        baseline_profiles_list = []
        controlled_profiles_list = []

        start_hour = 16
        start_minute = 0

        lines = len(baseline_profiles)
        for line in range(lines):
            for i in range(len(baseline_profiles[0])):
                hour_str = str((start_hour + line)% 24)
                minute = 15 * (i % 4)
                if minute is 0:
                    minute_str = '00'
                else:
                    minute_str = str(minute)

                baseline_profiles_list.append(
                    {
                        'time': hour_str + ':' + minute_str,
                        'load': str(baseline_profiles[line][i])
                    }
                )

                controlled_profiles_list.append(
                    {
                        'time': hour_str + ':' + minute_str,
                        'load': str(controlled_profiles[line][i])
                    }
                )

        cur.execute("INSERT INTO " + self.table_name + \
            " (county, rate_energy_peak, rate_energy_partpeak, rate_energy_offpeak," + \
            " rate_demand_peak, rate_demand_partpeak, rate_demand_overall, uncontrolled_load, controlled_load)" + \
            " VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
            (
                self.county, str(self.rate_energy_peak), str(self.rate_energy_partpeak), str(self.rate_energy_offpeak),
                str(self.rate_demand_peak), str(self.rate_demand_partpeak), str(self.rate_demand_overall), 
                json.dumps(baseline_profiles_list), json.dumps(controlled_profiles_list)
            )
        )

        print('Insertion finished...')
        # Make the changes to the database persistent
        conn.commit()

        # Close communication with the database
        cur.close()
        conn.close()