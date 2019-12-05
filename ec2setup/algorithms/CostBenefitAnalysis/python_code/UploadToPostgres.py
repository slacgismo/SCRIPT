import boto3
import json
import csv
import psycopg2


class UploadToPostgres():
    def __init__(
        self
    ): 
        self.result_dir = '/home/ubuntu/SCRIPT/ec2setup/algorithms/CostBenefitAnalysis/cases/basecase/results/'

        with open('postgres_info.json') as json_file:
            postgres_info = json.load(json_file)
        
        # loadprofile related
        self.load_profile_year_len = 0
        self.load_profile_result_dict = {}
        self.load_profile_start_year = 0
        with open(self.result_dir + 'aggregate_loadprofile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.load_profile_result_dict['All'] = {}
            for row in csv_reader:
                if row[0] == 'Type':
                    self.load_profile_start_year = int(row[2])
                    self.load_profile_year_len = len(row) - 2

                if row[0] not in self.load_profile_result_dict['All'].keys():
                    self.load_profile_result_dict['All'][row[0]] = {}

                self.load_profile_result_dict['All'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.load_profile_result_dict['All'][row[0]][row[1]].append(row[i])

        with open(self.result_dir + 'AllDCFC_loadprofile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.load_profile_result_dict['DC Fast Charger'] = {}
            for row in csv_reader:
                if row[0] not in self.load_profile_result_dict['DC Fast Charger'].keys():
                    self.load_profile_result_dict['DC Fast Charger'][row[0]] = {}

                self.load_profile_result_dict['DC Fast Charger'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.load_profile_result_dict['DC Fast Charger'][row[0]][row[1]].append(row[i])
        
        with open(self.result_dir + 'AllPublicL2_loadprofile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.load_profile_result_dict['Public L2'] = {}
            for row in csv_reader:
                if row[0] not in self.load_profile_result_dict['Public L2'].keys():
                    self.load_profile_result_dict['Public L2'][row[0]] = {}
                self.load_profile_result_dict['Public L2'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.load_profile_result_dict['Public L2'][row[0]][row[1]].append(row[i])
        
        with open(self.result_dir + 'AllResidential_loadprofile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.load_profile_result_dict['Residential'] = {}
            for row in csv_reader:
                if row[0] not in self.load_profile_result_dict['Residential'].keys():
                    self.load_profile_result_dict['Residential'][row[0]] = {}
                self.load_profile_result_dict['Residential'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.load_profile_result_dict['Residential'][row[0]][row[1]].append(row[i])

        with open(self.result_dir + 'AllWorkplace_loadprofile.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.load_profile_result_dict['Workplace'] = {}
            for row in csv_reader:
                if row[0] not in self.load_profile_result_dict['Workplace'].keys():
                    self.load_profile_result_dict['Workplace'][row[0]] = {}
                self.load_profile_result_dict['Workplace'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.load_profile_result_dict['Workplace'][row[0]][row[1]].append(row[i])

        # gas consumption result related 
        self.gas_consumption_year_len = 0
        self.gas_consumption_result_dict = {}
        with open(self.result_dir + 'annual_gas_consumption.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.gas_consumption_year_len = len(row) - 1
                self.gas_consumption_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.gas_consumption_result_dict[row[0]].append(row[i])

        # cost benefit result related 
        self.cost_benefit_year_len = 0
        self.cost_benefit_result_dict = {}
        with open(self.result_dir + 'annual_results.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.cost_benefit_year_len = len(row) - 1
                self.cost_benefit_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.cost_benefit_result_dict[row[0]].append(row[i])
                if "EV sales as " in row[0]:
                    fill_up_value = [row[1], row[2]]
                    for j in range(5):
                        self.cost_benefit_result_dict[row[0]].append(fill_up_value[0])
                        self.cost_benefit_result_dict[row[0]].append(fill_up_value[1])

        # emission result related 
        self.emission_year_len = 0
        self.emission_result_dict = {}
        with open(self.result_dir + 'Emissions.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.emission_year_len = len(row) - 1
                self.emission_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.emission_result_dict[row[0]].append(row[i])

        # npv result related
        self.npv_result_dict = {}
        with open(self.result_dir + 'npv_results.csv') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif line_count == 1:
                    self.npv_result_dict["Utility Bills"] = str(row[1])
                    line_count += 1
                elif line_count == 2:
                    self.npv_result_dict["Utility Bills (volumetric)"] = str(row[1])
                    line_count += 1
                elif line_count == 3:
                    self.npv_result_dict["Utility Bills (demand)"] = str(row[1])
                    line_count += 1
                elif line_count == 4:
                    self.npv_result_dict["Utility Bills (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 5:
                    self.npv_result_dict["Utility Bills (work)"] = str(row[1])
                    line_count += 1
                elif line_count == 6:
                    self.npv_result_dict["Utility Bills (pub L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 7:
                    self.npv_result_dict["Utility Bills (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 8:
                    self.npv_result_dict["Incremental upfront vehicle cost"] = str(row[1])
                    line_count += 1
                elif line_count == 9:
                    self.npv_result_dict["Charging infrastructure cost"] = str(row[1])
                    line_count += 1
                elif line_count == 10:
                    self.npv_result_dict["Charging infrastructure cost (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 11:
                    self.npv_result_dict["Charging infrastructure cost (work L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 12:
                    self.npv_result_dict["Charging infrastructure cost (public L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 13:
                    self.npv_result_dict["Charging infrastructure cost (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 14:
                    self.npv_result_dict["Avoided vehicle gasoline"] = str(row[1])
                    line_count += 1
                elif line_count == 15:
                    self.npv_result_dict["Vehicle O&M Savings"] = str(row[1])
                    line_count += 1
                elif line_count == 16:
                    self.npv_result_dict["Federal EV Tax Credit"] = str(row[1])
                    line_count += 1
                elif line_count == 17:
                    self.npv_result_dict["Energy Supply Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 18:
                    self.npv_result_dict["Energy Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 19:
                    self.npv_result_dict["Generation Capacity Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 20:
                    self.npv_result_dict["Vehicle Sales (NPV)"] = str(row[1])
                    line_count += 1
                elif line_count == 21:
                    self.npv_result_dict["Transmission and Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 22:
                    self.npv_result_dict["Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 23:
                    self.npv_result_dict["Transmission Cost"] = str(row[1])
                    line_count += 1
                

        self.db_host = postgres_info['DB_HOST']
        self.cba_net_present_table_name = "script_algorithm_cba_net_present_value"
        self.gas_consumption_table_name = "script_algorithm_cba_gas_consumption"
        self.cba_net_emission_table_name = "script_algorithm_cba_net_emission"
        self.cba_cost_benefit_table_name = "script_algorithm_cba_cost_benefit"
        self.cba_load_profile_table_name = "script_algorithm_cba_load_profile"

        self.postgres_db = postgres_info['POSTGRES_DB']
        self.postgres_user = postgres_info['POSTGRES_USER']
        self.postgres_password = postgres_info['POSTGRES_PASSWORD']
        
        self.conn = psycopg2.connect(
            host=self.db_host,
            dbname=self.postgres_db,
            user=self.postgres_user,
            password=self.postgres_password,
            port='5432'
        )

        self.cur = self.conn.cursor()

        self.run_load_profile()
        self.run_cost_benefit()
        self.run_gas_consumption()
        self.run_npv()
        self.run_emission()

        # Close communication with the database
        self.cur.close()
        self.conn.close()


    def run_load_profile(self):
        # create table on Postgres
        # self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.cba_load_profile_table_name + " (id serial PRIMARY KEY, config_id INTEGER, poi varchar, year INTEGER, day_type varchar, loads varchar);")

        tmp_load = {}

        for i in range(self.load_profile_year_len):
            for poi in self.load_profile_result_dict.keys():
                tmp_load[poi] = {}
                cur_year = str(self.load_profile_start_year + i)
                tmp_load[poi][cur_year] = {}
                for day_type in self.load_profile_result_dict[poi].keys():
                    if day_type != "Type":
                        tmp_load[poi][cur_year][day_type] = []
                        for hour in self.load_profile_result_dict[poi][day_type].keys():
                            tmp_load[poi][cur_year][day_type].append(
                                self.load_profile_result_dict[poi][day_type][hour][i]
                            )
                        self.cur.execute("INSERT INTO " + self.cba_load_profile_table_name + " (config_id, poi, year, day_type, loads) VALUES (%s, %s, %s, %s, %s)",
                            (
                                '1', str(poi), int(cur_year), str(day_type), json.dumps(tmp_load[poi][cur_year][day_type])
                            )
                        )

        print('Insertion finished...')
        # Make the changes to the database persistent
        self.conn.commit()
    

    def run_cost_benefit(self):
        # create table on Postgres
        # self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.cba_cost_benefit_table_name + " (id serial PRIMARY KEY, config_id INTEGER, year INTEGER, cost_benefit varchar);")

        for i in range(self.cost_benefit_year_len):
            tmp_res = {}

            for key in self.cost_benefit_result_dict.keys():
                if key != 'Year':
                    tmp_res[key] = self.cost_benefit_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.cba_cost_benefit_table_name + " (config_id, year, cost_benefit) VALUES (%s, %s, %s)",
                (
                    '1', str(self.cost_benefit_result_dict['Year'][i]), json.dumps(tmp_res)
                )
            )

        print('Insertion finished...')
        # Make the changes to the database persistent
        self.conn.commit()


    def run_gas_consumption(self):

        # create table on Postgres
        # self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.gas_consumption_table_name + " (id serial PRIMARY KEY, config_id INTEGER, year INTEGER, consumption varchar);")

        for i in range(self.gas_consumption_year_len):
            tmp_res = {}

            for key in self.gas_consumption_result_dict.keys():
                if key != 'Year':
                    tmp_res[key] = self.gas_consumption_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.gas_consumption_table_name + " (config_id, year, consumption) VALUES (%s, %s, %s)",
                (
                    '1', str(self.gas_consumption_result_dict['Year'][i]), json.dumps(tmp_res)
                )
            )

        print('Insertion finished...')
        # Make the changes to the database persistent
        self.conn.commit()


    def run_npv(self):

        # create table on Postgres
        # self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.cba_net_present_table_name + " (id serial PRIMARY KEY, config_id INTEGER, year INTEGER, npv varchar);")

        self.cur.execute("INSERT INTO " + self.cba_net_present_table_name + " (config_id, year, npv) VALUES (%s, %s, %s)",
            (
                '1', '2020', json.dumps(self.npv_result_dict)
            )
        )

        print('Insertion finished...')
        # Make the changes to the database persistent
        self.conn.commit()
    
    def run_emission(self):
        # create table on Postgres
        # self.cur.execute("CREATE TABLE IF NOT EXISTS " + self.cba_net_emission_table_name + " (id serial PRIMARY KEY, config_id INTEGER, year INTEGER, emissions varchar);")

        for i in range(self.emission_year_len):
            tmp_res = {}

            for key in self.emission_result_dict.keys():
                if key != 'Year':
                    tmp_res[key] = self.emission_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.cba_net_emission_table_name + " (config_id, year, emissions) VALUES (%s, %s, %s)",
                (
                    '1', str(self.emission_result_dict['Year'][i]), json.dumps(tmp_res)
                )
            )

        print('Insertion finished...')
        # Make the changes to the database persistent
        self.conn.commit()

