from __future__ import unicode_literals
import boto3
import json
import csv
import psycopg2
from itertools import zip_longest
from django.conf import settings


class UploadToPostgres():
    def __init__(
        self,
        load_profile,
        county
    ):

        with open(settings.BASE_DIR + '/postgres_info.json') as json_file:
            postgres_info = json.load(json_file)

        self.db_host = postgres_info['DB_HOST']
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


        # load_profile related
        self.load_profile_year_len = 0
        self.uncontrolled_load_profile_result_dict = {}
        self.controlled_load_profile_result_dict = {}
        self.load_profile_start_year = 0
        self.load_profile = load_profile
        self.county = county

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/aggregate_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.uncontrolled_load_profile_result_dict['All'] = {}
            for row in csv_reader:
                if row[0] == 'Type':
                    self.load_profile_start_year = int(row[2])
                    self.load_profile_year_len = len(row) - 2

                if row[0] not in self.uncontrolled_load_profile_result_dict['All'].keys():
                    self.uncontrolled_load_profile_result_dict['All'][row[0]] = {}

                self.uncontrolled_load_profile_result_dict['All'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.uncontrolled_load_profile_result_dict['All'][row[0]][row[1]].append(row[i])
        
        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/aggregate_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.controlled_load_profile_result_dict['All'] = {}
            for row in csv_reader:
                if row[0] not in self.controlled_load_profile_result_dict['All'].keys():
                    self.controlled_load_profile_result_dict['All'][row[0]] = {}

                self.controlled_load_profile_result_dict['All'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.controlled_load_profile_result_dict['All'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/AllDCFC_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.uncontrolled_load_profile_result_dict['DC Fast Charger'] = {}
            for row in csv_reader:
                if row[0] not in self.uncontrolled_load_profile_result_dict['DC Fast Charger'].keys():
                    self.uncontrolled_load_profile_result_dict['DC Fast Charger'][row[0]] = {}

                self.uncontrolled_load_profile_result_dict['DC Fast Charger'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.uncontrolled_load_profile_result_dict['DC Fast Charger'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/AllDCFC_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.controlled_load_profile_result_dict['DC Fast Charger'] = {}
            for row in csv_reader:
                if row[0] not in self.controlled_load_profile_result_dict['DC Fast Charger'].keys():
                    self.controlled_load_profile_result_dict['DC Fast Charger'][row[0]] = {}

                self.controlled_load_profile_result_dict['DC Fast Charger'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.controlled_load_profile_result_dict['DC Fast Charger'][row[0]][row[1]].append(row[i])
        
        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/AllPublicL2_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.uncontrolled_load_profile_result_dict['Public L2'] = {}
            for row in csv_reader:
                if row[0] not in self.uncontrolled_load_profile_result_dict['Public L2'].keys():
                    self.uncontrolled_load_profile_result_dict['Public L2'][row[0]] = {}
                self.uncontrolled_load_profile_result_dict['Public L2'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.uncontrolled_load_profile_result_dict['Public L2'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/AllPublicL2_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.controlled_load_profile_result_dict['Public L2'] = {}
            for row in csv_reader:
                if row[0] not in self.controlled_load_profile_result_dict['Public L2'].keys():
                    self.controlled_load_profile_result_dict['Public L2'][row[0]] = {}
                self.controlled_load_profile_result_dict['Public L2'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.controlled_load_profile_result_dict['Public L2'][row[0]][row[1]].append(row[i])
        
        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/AllResidential_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.uncontrolled_load_profile_result_dict['Residential'] = {}
            for row in csv_reader:
                if row[0] not in self.uncontrolled_load_profile_result_dict['Residential'].keys():
                    self.uncontrolled_load_profile_result_dict['Residential'][row[0]] = {}
                self.uncontrolled_load_profile_result_dict['Residential'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.uncontrolled_load_profile_result_dict['Residential'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/AllResidential_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.controlled_load_profile_result_dict['Residential'] = {}
            for row in csv_reader:
                if row[0] not in self.controlled_load_profile_result_dict['Residential'].keys():
                    self.controlled_load_profile_result_dict['Residential'][row[0]] = {}
                self.controlled_load_profile_result_dict['Residential'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.controlled_load_profile_result_dict['Residential'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/AllWorkplace_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.uncontrolled_load_profile_result_dict['Workplace'] = {}
            for row in csv_reader:
                if row[0] not in self.uncontrolled_load_profile_result_dict['Workplace'].keys():
                    self.uncontrolled_load_profile_result_dict['Workplace'][row[0]] = {}
                self.uncontrolled_load_profile_result_dict['Workplace'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.uncontrolled_load_profile_result_dict['Workplace'][row[0]][row[1]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/AllWorkplace_loadprofile.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            self.controlled_load_profile_result_dict['Workplace'] = {}
            for row in csv_reader:
                if row[0] not in self.controlled_load_profile_result_dict['Workplace'].keys():
                    self.controlled_load_profile_result_dict['Workplace'][row[0]] = {}
                self.controlled_load_profile_result_dict['Workplace'][row[0]][row[1]] = []
                for i in range(2, len(row)):
                    self.controlled_load_profile_result_dict['Workplace'][row[0]][row[1]].append(row[i])

        # gas consumption result related 
        self.gas_consumption_year_len = 0
        self.uncontrolled_gas_consumption_result_dict = {}
        self.controlled_gas_consumption_result_dict = {}

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/annual_gas_consumption.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.gas_consumption_year_len = len(row) - 1
                self.uncontrolled_gas_consumption_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.uncontrolled_gas_consumption_result_dict[row[0]].append(row[i])
        
        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/annual_gas_consumption.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.controlled_gas_consumption_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.controlled_gas_consumption_result_dict[row[0]].append(row[i])

        # cost benefit result related 
        self.cost_benefit_year_len = 0
        self.uncontrolled_cost_benefit_result_dict = {}
        self.controlled_cost_benefit_result_dict = {}

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/annual_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.cost_benefit_year_len = len(row) - 1
                self.uncontrolled_cost_benefit_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.uncontrolled_cost_benefit_result_dict[row[0]].append(row[i])
                if "EV sales as " in row[0]:
                    fill_up_value = [row[1], row[2]]
                    for j in range(5):
                        self.uncontrolled_cost_benefit_result_dict[row[0]].append(fill_up_value[0])
                        self.uncontrolled_cost_benefit_result_dict[row[0]].append(fill_up_value[1])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/annual_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.controlled_cost_benefit_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.controlled_cost_benefit_result_dict[row[0]].append(row[i])
                if "EV sales as " in row[0]:
                    fill_up_value = [row[1], row[2]]
                    for j in range(5):
                        self.controlled_cost_benefit_result_dict[row[0]].append(fill_up_value[0])
                        self.controlled_cost_benefit_result_dict[row[0]].append(fill_up_value[1])

        # emission result related 
        self.emission_year_len = 0
        self.uncontrolled_emission_result_dict = {}
        self.controlled_emission_result_dict = {}

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/Emissions.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.emission_year_len = len(row) - 1
                self.uncontrolled_emission_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.uncontrolled_emission_result_dict[row[0]].append(row[i])

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/Emissions.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                self.controlled_emission_result_dict[row[0]] = []
                for i in range(1, len(row)):
                    self.controlled_emission_result_dict[row[0]].append(row[i])

        # npv result related
        self.uncontrolled_npv_result_dict = {}
        self.controlled_npv_result_dict = {}

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/npv_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif line_count == 1:
                    self.uncontrolled_npv_result_dict["Utility Bills"] = str(row[1])
                    line_count += 1
                elif line_count == 2:
                    self.uncontrolled_npv_result_dict["Utility Bills (volumetric)"] = str(row[1])
                    line_count += 1
                elif line_count == 3:
                    self.uncontrolled_npv_result_dict["Utility Bills (demand)"] = str(row[1])
                    line_count += 1
                elif line_count == 4:
                    self.uncontrolled_npv_result_dict["Utility Bills (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 5:
                    self.uncontrolled_npv_result_dict["Utility Bills (work)"] = str(row[1])
                    line_count += 1
                elif line_count == 6:
                    self.uncontrolled_npv_result_dict["Utility Bills (pub L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 7:
                    self.uncontrolled_npv_result_dict["Utility Bills (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 8:
                    self.uncontrolled_npv_result_dict["Incremental upfront vehicle cost"] = str(row[1])
                    line_count += 1
                elif line_count == 9:
                    self.uncontrolled_npv_result_dict["Charging infrastructure cost"] = str(row[1])
                    line_count += 1
                elif line_count == 10:
                    self.uncontrolled_npv_result_dict["Charging infrastructure cost (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 11:
                    self.uncontrolled_npv_result_dict["Charging infrastructure cost (work L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 12:
                    self.uncontrolled_npv_result_dict["Charging infrastructure cost (public L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 13:
                    self.uncontrolled_npv_result_dict["Charging infrastructure cost (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 14:
                    self.uncontrolled_npv_result_dict["Avoided vehicle gasoline"] = str(row[1])
                    line_count += 1
                elif line_count == 15:
                    self.uncontrolled_npv_result_dict["Vehicle O&M Savings"] = str(row[1])
                    line_count += 1
                elif line_count == 16:
                    self.uncontrolled_npv_result_dict["Federal EV Tax Credit"] = str(row[1])
                    line_count += 1
                elif line_count == 17:
                    self.uncontrolled_npv_result_dict["Energy Supply Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 18:
                    self.uncontrolled_npv_result_dict["Energy Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 19:
                    self.uncontrolled_npv_result_dict["Generation Capacity Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 20:
                    self.uncontrolled_npv_result_dict["Vehicle Sales (NPV)"] = str(row[1])
                    line_count += 1
                elif line_count == 21:
                    self.uncontrolled_npv_result_dict["Transmission and Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 22:
                    self.uncontrolled_npv_result_dict["Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 23:
                    self.uncontrolled_npv_result_dict["Transmission Cost"] = str(row[1])
                    line_count += 1

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/npv_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                elif line_count == 1:
                    self.controlled_npv_result_dict["Utility Bills"] = str(row[1])
                    line_count += 1
                elif line_count == 2:
                    self.controlled_npv_result_dict["Utility Bills (volumetric)"] = str(row[1])
                    line_count += 1
                elif line_count == 3:
                    self.controlled_npv_result_dict["Utility Bills (demand)"] = str(row[1])
                    line_count += 1
                elif line_count == 4:
                    self.controlled_npv_result_dict["Utility Bills (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 5:
                    self.controlled_npv_result_dict["Utility Bills (work)"] = str(row[1])
                    line_count += 1
                elif line_count == 6:
                    self.controlled_npv_result_dict["Utility Bills (pub L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 7:
                    self.controlled_npv_result_dict["Utility Bills (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 8:
                    self.controlled_npv_result_dict["Incremental upfront vehicle cost"] = str(row[1])
                    line_count += 1
                elif line_count == 9:
                    self.controlled_npv_result_dict["Charging infrastructure cost"] = str(row[1])
                    line_count += 1
                elif line_count == 10:
                    self.controlled_npv_result_dict["Charging infrastructure cost (res)"] = str(row[1])
                    line_count += 1
                elif line_count == 11:
                    self.controlled_npv_result_dict["Charging infrastructure cost (work L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 12:
                    self.controlled_npv_result_dict["Charging infrastructure cost (public L2)"] = str(row[1])
                    line_count += 1
                elif line_count == 13:
                    self.controlled_npv_result_dict["Charging infrastructure cost (DCFC)"] = str(row[1])
                    line_count += 1
                elif line_count == 14:
                    self.controlled_npv_result_dict["Avoided vehicle gasoline"] = str(row[1])
                    line_count += 1
                elif line_count == 15:
                    self.controlled_npv_result_dict["Vehicle O&M Savings"] = str(row[1])
                    line_count += 1
                elif line_count == 16:
                    self.controlled_npv_result_dict["Federal EV Tax Credit"] = str(row[1])
                    line_count += 1
                elif line_count == 17:
                    self.controlled_npv_result_dict["Energy Supply Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 18:
                    self.controlled_npv_result_dict["Energy Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 19:
                    self.controlled_npv_result_dict["Generation Capacity Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 20:
                    self.controlled_npv_result_dict["Vehicle Sales (NPV)"] = str(row[1])
                    line_count += 1
                elif line_count == 21:
                    self.controlled_npv_result_dict["Transmission and Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 22:
                    self.controlled_npv_result_dict["Distribution Cost"] = str(row[1])
                    line_count += 1
                elif line_count == 23:
                    self.controlled_npv_result_dict["Transmission Cost"] = str(row[1])
                    line_count += 1

        self.cba_net_present_table_name = "script_algorithm_cba_net_present_value"
        self.gas_consumption_table_name = "script_algorithm_cba_gas_consumption"
        self.cba_emission_table_name = "script_algorithm_cba_emission"
        self.cba_cost_benefit_table_name = "script_algorithm_cba_cost_benefit"
        self.cba_load_profile_table_name = "script_algorithm_cba_load_profile"
        self.config_cba_net_present_table_name = "script_config_cba_net_present_value"
        self.config_gas_consumption_table_name = "script_config_cba_gas_consumption"
        self.config_cba_emission_table_name = "script_config_cba_emission"
        self.config_cba_cost_benefit_table_name = "script_config_cba_cost_benefit"
        self.config_cba_load_profile_table_name = "script_config_cba_load_profile"

        self.cur = self.conn.cursor()

        self.run_load_profile()
        self.run_cost_benefit()
        self.run_gas_consumption()
        self.run_npv()
        self.run_emission()

        # Close communication with the database
        self.cur.close()
        self.conn.close()

        print("Cost Benefit Analysis Runner completed successfully.")


    def run_load_profile(self):

        uncontrolled_tmp_load = {}
        controlled_tmp_load = {}

        for i in range(self.load_profile_year_len):
        
            for uncontrolled_poi, controlled_poi in zip_longest(self.uncontrolled_load_profile_result_dict.keys(), self.controlled_load_profile_result_dict.keys()):
                
                uncontrolled_tmp_load[uncontrolled_poi] = {}
                controlled_tmp_load[controlled_poi] = {}
                
                cur_year = str(self.load_profile_start_year + i)
                
                uncontrolled_tmp_load[uncontrolled_poi][cur_year] = {}
                controlled_tmp_load[controlled_poi][cur_year] = {}

                for uncontrolled_day_type, controlled_day_type in zip_longest(self.uncontrolled_load_profile_result_dict[uncontrolled_poi].keys(), self.controlled_load_profile_result_dict[controlled_poi].keys()):
                    if uncontrolled_day_type != "Type" and controlled_day_type != "Type":

                        uncontrolled_tmp_load[uncontrolled_poi][cur_year][uncontrolled_day_type] = []
                        for hour in self.uncontrolled_load_profile_result_dict[uncontrolled_poi][uncontrolled_day_type].keys():
                            uncontrolled_tmp_load[uncontrolled_poi][cur_year][uncontrolled_day_type].append(
                                self.uncontrolled_load_profile_result_dict[uncontrolled_poi][uncontrolled_day_type][hour][i]
                            )

                        controlled_tmp_load[controlled_poi][cur_year][controlled_day_type] = []
                        for hour in self.controlled_load_profile_result_dict[controlled_poi][controlled_day_type].keys():
                            controlled_tmp_load[controlled_poi][cur_year][controlled_day_type].append(
                                self.controlled_load_profile_result_dict[controlled_poi][controlled_day_type][hour][i]
                            )

                        self.cur.execute("INSERT INTO " + self.config_cba_load_profile_table_name + " (lf_config, poi, year, day_type) VALUES (%s, %s, %s, %s)",
                            (
                                self.load_profile, str(uncontrolled_poi), int(cur_year), str(uncontrolled_day_type)
                            )
                        )

                        self.conn.commit()

                        #query for the id of the config table
                        self.cur.execute("SELECT id FROM "+self.config_cba_load_profile_table_name + " ORDER BY id DESC LIMIT 1")
                        config_load_profile_id = self.cur.fetchone()[0]

                        self.cur.execute("INSERT INTO " + self.cba_load_profile_table_name + " (config, controlled_values, uncontrolled_values) VALUES (%s, %s, %s)",
                            (
                                str(config_load_profile_id), json.dumps(uncontrolled_tmp_load[uncontrolled_poi][cur_year][uncontrolled_day_type]), json.dumps(controlled_tmp_load[controlled_poi][cur_year][controlled_day_type])
                            )
                        )

        # Make the changes to the database persistent
        self.conn.commit()
    

    def run_cost_benefit(self):

        for i in range(self.cost_benefit_year_len):
            uncontrolled_tmp_res = {}
            controlled_tmp_res = {}

            for key in self.uncontrolled_cost_benefit_result_dict.keys():
                if key != 'Year':
                    uncontrolled_tmp_res[key] = self.uncontrolled_cost_benefit_result_dict[key][i]
            
            for key in self.controlled_cost_benefit_result_dict.keys():
                if key != 'Year':
                    controlled_tmp_res[key] = self.controlled_cost_benefit_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.config_cba_cost_benefit_table_name + " (lf_config, year) VALUES (%s, %s)",
                (
                    self.load_profile, str(self.uncontrolled_cost_benefit_result_dict['Year'][i])
                )
            )
            self.conn.commit()

            self.cur.execute("SELECT id FROM "+self.config_cba_cost_benefit_table_name + " ORDER BY id DESC LIMIT 1")
            config_cost_benefit_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.cba_cost_benefit_table_name + " (config, uncontrolled_values, controlled_values) VALUES (%s, %s, %s)",
                (
                    str(config_cost_benefit_id), json.dumps(uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                )
            )

        # Make the changes to the database persistent
        self.conn.commit()


    def run_gas_consumption(self):

        for i in range(self.gas_consumption_year_len):
            uncontrolled_tmp_res = {}
            controlled_tmp_res = {}

            for key in self.uncontrolled_gas_consumption_result_dict.keys():
                if key != 'Year':
                    uncontrolled_tmp_res[key] = self.uncontrolled_gas_consumption_result_dict[key][i]
            
            for key in self.controlled_gas_consumption_result_dict.keys():
                if key != 'Year':
                    controlled_tmp_res[key] = self.controlled_gas_consumption_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.config_gas_consumption_table_name + " (lf_config, year) VALUES (%s, %s)",
                (
                    self.load_profile, str(self.uncontrolled_gas_consumption_result_dict['Year'][i])
                )
            )

            self.conn.commit()

            self.cur.execute("SELECT id FROM "+self.config_gas_consumption_table_name + " ORDER BY id DESC LIMIT 1")
            config_gas_consumption_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.gas_consumption_table_name + " (config, controlled_values, uncontrolled_values) VALUES (%s, %s, %s)",
                (
                    str(config_gas_consumption_id), json.dumps(uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                )
            )

        # Make the changes to the database persistent
        self.conn.commit()


    def run_npv(self):

        self.cur.execute("INSERT INTO " + self.config_cba_net_present_table_name + " (lf_config, year) VALUES (%s, %s)",
            (
                self.load_profile, "2020"
            )
        )

        self.conn.commit()

        self.cur.execute("SELECT id FROM "+self.config_cba_net_present_table_name + " ORDER BY id DESC LIMIT 1")
        config_net_present_id = self.cur.fetchone()[0]
        
        self.cur.execute("INSERT INTO " + self.cba_net_present_table_name + " (config, uncontrolled_values, controlled_values) VALUES (%s, %s, %s)",
            (
                str(config_net_present_id), json.dumps(self.uncontrolled_npv_result_dict), json.dumps(self.controlled_npv_result_dict)
            )
        )

        # Make the changes to the database persistent
        self.conn.commit()
    
    def run_emission(self):

        for i in range(self.emission_year_len):
            uncontrolled_tmp_res = {}
            controlled_tmp_res = {}

            for key in self.uncontrolled_emission_result_dict.keys():
                if key != 'Year':
                    uncontrolled_tmp_res[key] = self.uncontrolled_emission_result_dict[key][i]
            
            for key in self.controlled_emission_result_dict.keys():
                if key != 'Year':
                    controlled_tmp_res[key] = self.controlled_emission_result_dict[key][i]
            
            self.cur.execute("INSERT INTO " + self.config_cba_emission_table_name + " (lf_config, year) VALUES (%s, %s)",
                (
                    self.load_profile, str(self.uncontrolled_emission_result_dict['Year'][i])
                )
            )

            self.conn.commit()

            self.cur.execute("SELECT id FROM "+self.config_cba_emission_table_name + " ORDER BY id DESC LIMIT 1")
            config_emission_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.cba_emission_table_name + " (config, uncontrolled_values, controlled_values) VALUES (%s, %s, %s)",
                (
                    str(config_emission_id), json.dumps(uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                )
            )

        # Make the changes to the database persistent
        self.conn.commit()
