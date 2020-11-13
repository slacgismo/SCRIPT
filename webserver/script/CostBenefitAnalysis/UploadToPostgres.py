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

        self.load_profile = load_profile
        self.county = county


        # gas consumption result related
        self.gas_consumption_year_len = 0
        self.uncontrolled_gas_consumption_result_dict = {}
        self.controlled_gas_consumption_result_dict = {}

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/annual_gas_consumption.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == 'Year' or row[0] == 'EV Share (%)':
                    self.uncontrolled_gas_consumption_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.uncontrolled_gas_consumption_result_dict[row[0]].append(
                            item)

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/annual_gas_consumption.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == 'Year' or row[0] == 'EV Share (%)':
                    self.controlled_gas_consumption_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.controlled_gas_consumption_result_dict[row[0]].append(
                            item)


        # emission result related
        self.emission_year_len = 0
        self.uncontrolled_emission_result_dict = {}
        self.controlled_emission_result_dict = {}
        self.uncontrolled_co2_emissions = []
        self.controlled_co2_emissions = []

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/Emissions.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == 'CO2 emissions from EVs (metric tons)':
                    self.uncontrolled_emission_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.uncontrolled_emission_result_dict[row[0]].append(item)
                        self.uncontrolled_co2_emissions.append(item)

                if row[0] == 'NOX emissions from EVs (metric tons)'or row[0] == 'Year' or row[0] == 'PM 10 emissions from EVs (metric tons)':
                    self.uncontrolled_emission_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.uncontrolled_emission_result_dict[row[0]].append(item)

        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/Emissions.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == 'CO2 emissions from EVs (metric tons)':
                    self.controlled_emission_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.controlled_emission_result_dict[row[0]].append(item)
                        self.controlled_co2_emissions.append(item)

                if row[0] == 'NOX emissions from EVs (metric tons)' or row[0] == 'Year' or row[0] == 'PM 10 emissions from EVs (metric tons)':
                    self.controlled_emission_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.controlled_emission_result_dict[row[0]].append(item)


        # cost benefit result related
        self.cost_benefit_year_len = 0
        self.uncontrolled_cost_benefit_result_dict = {}
        self.controlled_cost_benefit_result_dict = {}
        self.uncontrolled_electricity_supply_cost_list = []
        self.controlled_electricity_supply_cost_list = []
        self.uncontrolled_avoided_gasoline_gallons = []
        self.controlled_avoided_gasoline_gallons = []
        
        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_uncontrolled_load/results/annual_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:
                if row[0] == 'Energy Supply Cost' or row[0] == 'Capacity Cost' or row[0] == 'Distribution Cost' or row[0] == 'Transmission Cost' or row[0] == 'GHG Cost':
                    for idx, item in enumerate(row[1:]):
                        if len(self.uncontrolled_electricity_supply_cost_list) > idx:
                            self.uncontrolled_electricity_supply_cost_list[idx] = self.uncontrolled_electricity_supply_cost_list[idx] + float(item)
                        else:
                            self.uncontrolled_electricity_supply_cost_list.append(float(item))
                    self.uncontrolled_cost_benefit_result_dict['Electricity Supply Cost'] = [str(item) for item in self.uncontrolled_electricity_supply_cost_list]
                
                if row[0] == 'Utility Bills' or row[0] == 'Year' or row[0] == 'Cumulative personal light-duty EV population':
                    self.uncontrolled_cost_benefit_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.uncontrolled_cost_benefit_result_dict[row[0]].append(item)

                if row[0] == 'Avoided vehicle gasoline (gallons)':
                    self.uncontrolled_cost_benefit_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.uncontrolled_cost_benefit_result_dict[row[0]].append(item)
                        self.uncontrolled_avoided_gasoline_gallons.append(item)

            self.uncontrolled_cost_benefit_result_dict['Net Carbon Emission Savings ($)'] = []
            for idx, item in enumerate(self.uncontrolled_avoided_gasoline_gallons):
                co2_savings = float(item) * 0.008887 - float(self.uncontrolled_co2_emissions[idx])
                self.uncontrolled_cost_benefit_result_dict['Net Carbon Emission Savings ($)'].append(str(co2_savings))


        with open(settings.BASE_DIR[:-3] + 'script/CostBenefitAnalysis/cases/BaseCase_{0}_e19controlled_load/results/annual_results.csv'.format(county)) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            for row in csv_reader:    
                if row[0] == 'Energy Supply Cost' or row[0] == 'Capacity Cost' or row[0] == 'Distribution Cost' or row[0] == 'Transmission Cost' or row[0] == 'GHG Cost':
                    for idx, item in enumerate(row[1:]):
                        if len(self.controlled_electricity_supply_cost_list) > idx:
                            self.controlled_electricity_supply_cost_list[idx] = self.controlled_electricity_supply_cost_list[idx] + float(item)
                        else:
                            self.controlled_electricity_supply_cost_list.append(float(item))
                    self.controlled_cost_benefit_result_dict['Electricity Supply Cost'] = [str(item) for item in self.controlled_electricity_supply_cost_list]
                
                if row[0] == 'Utility Bills' or row[0] == 'Year' or row[0] == 'Cumulative personal light-duty EV population':
                    self.controlled_cost_benefit_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.controlled_cost_benefit_result_dict[row[0]].append(item)

                if row[0] == 'Avoided vehicle gasoline (gallons)':
                    self.controlled_cost_benefit_result_dict[row[0]] = []
                    for item in row[1:]:
                        self.controlled_cost_benefit_result_dict[row[0]].append(item)
                        self.controlled_avoided_gasoline_gallons.append(item)
            
            self.controlled_cost_benefit_result_dict['Net Carbon Emission Savings ($)'] = []
            for idx, item in enumerate(self.controlled_avoided_gasoline_gallons):
                co2_savings = float(item) * 0.008887 - float(self.controlled_co2_emissions[idx])
                self.controlled_cost_benefit_result_dict['Net Carbon Emission Savings ($)'].append(str(co2_savings))

        self.gas_consumption_table_name = "script_algorithm_cba_gas_consumption"
        self.cba_emission_table_name = "script_algorithm_cba_emission"
        self.cba_cost_benefit_table_name = "script_algorithm_cba_cost_benefit"
        self.config_gas_consumption_table_name = "script_config_cba_gas_consumption"
        self.config_cba_emission_table_name = "script_config_cba_emission"
        self.config_cba_cost_benefit_table_name = "script_config_cba_cost_benefit"

        self.cur = self.conn.cursor()

        self.run_cost_benefit()
        self.run_gas_consumption()
        self.run_emission()

        # Close communication with the database
        self.cur.close()
        self.conn.close()

        print("Cost Benefit Analysis Runner completed successfully.")

    def run_cost_benefit(self):

        print(self.uncontrolled_cost_benefit_result_dict)
        print(self.controlled_cost_benefit_result_dict)
        for i in range(11):
            uncontrolled_tmp_res = {}
            controlled_tmp_res = {}

            for key in self.uncontrolled_cost_benefit_result_dict.keys():
                if key != 'Year':
                    print(key)
                    uncontrolled_tmp_res[key] = self.uncontrolled_cost_benefit_result_dict[key][i]

            for key in self.controlled_cost_benefit_result_dict.keys():
                if key != 'Year':
                    print(key)
                    controlled_tmp_res[key] = self.controlled_cost_benefit_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.config_cba_cost_benefit_table_name + " (lf_config, year) VALUES (%s, %s)",
                            (
                                self.load_profile, str(
                                    self.uncontrolled_cost_benefit_result_dict['Year'][i])
                            )
                            )
            self.conn.commit()

            self.cur.execute(
                "SELECT id FROM " + self.config_cba_cost_benefit_table_name + " ORDER BY id DESC LIMIT 1")
            config_cost_benefit_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.cba_cost_benefit_table_name + " (config, uncontrolled_values, controlled_values) VALUES (%s, %s, %s)",
                            (
                                str(config_cost_benefit_id), json.dumps(
                                    uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                            )
                            )

        # Make the changes to the database persistent
        self.conn.commit()

    def run_gas_consumption(self):

        for i in range(11):
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
                                 self.load_profile, str(
                                     self.uncontrolled_gas_consumption_result_dict['Year'][i])
                             )
                             )

            self.conn.commit()

            self.cur.execute(
                "SELECT id FROM "+self.config_gas_consumption_table_name + " ORDER BY id DESC LIMIT 1")
            config_gas_consumption_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.gas_consumption_table_name + " (config, controlled_values, uncontrolled_values) VALUES (%s, %s, %s)",
                             (
                                 str(config_gas_consumption_id), json.dumps(
                                     uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                             )
                             )

        # Make the changes to the database persistent
        self.conn.commit()

    def run_emission(self):

        for i in range(11):
            uncontrolled_tmp_res = {}
            controlled_tmp_res = {}

            for key in self.uncontrolled_emission_result_dict.keys():
                if key != 'Year':
                    print(key)
                    uncontrolled_tmp_res[key] = self.uncontrolled_emission_result_dict[key][i]

            for key in self.controlled_emission_result_dict.keys():
                if key != 'Year':
                    print(key)
                    controlled_tmp_res[key] = self.controlled_emission_result_dict[key][i]

            self.cur.execute("INSERT INTO " + self.config_cba_emission_table_name + " (lf_config, year) VALUES (%s, %s)",
                             (
                                 self.load_profile, str(
                                     self.uncontrolled_emission_result_dict['Year'][i])
                             )
                             )

            self.conn.commit()

            self.cur.execute(
                "SELECT id FROM "+self.config_cba_emission_table_name + " ORDER BY id DESC LIMIT 1")
            config_emission_id = self.cur.fetchone()[0]

            self.cur.execute("INSERT INTO " + self.cba_emission_table_name + " (config, uncontrolled_values, controlled_values) VALUES (%s, %s, %s)",
                             (
                                 str(config_emission_id), json.dumps(
                                     uncontrolled_tmp_res), json.dumps(controlled_tmp_res)
                             )
                             )

        # Make the changes to the database persistent
        self.conn.commit()
