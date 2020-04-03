from __future__ import division
from __future__ import unicode_literals
from past.utils import old_div
from builtins import range
from builtins import object
import copy
import constants
import helpers
from collections import Counter
class Vehicles(object):

    def __init__(self):

        self.population = {}
        self.total_population = {}
        self.new_sales = {}
        self.ldv_new_sales = {}
        self.replacements = {}
        self.ldv_replacements = {}
        self.first_replacement_year = int()
        self.adoption_years = []
        self.sales = {}
        self.ldv_sales = {}
        self.inc_prices = {}
        self.new_mpg = {}
        self.gas_prices = {}
        self.new_vmt = {}

        self.vehicle_lifetime = int()

        self.capital_cost = {}
        self.tax_credit = {}
        self.oandm_savings = {}
        self.bev_oandm_savings = {}
        self.phev_oandm_savings = {}
        self.mpg_improvement_factors = {}
        self.vmt_change_factor = {}
        self.gallons_avoided = {}
        self.co2_savings = {}
        self.gasoline_savings = {}
        self.gasoline_consumption = {}
        self.gasoline_consumption_mmbtu = {}
        self.gasoline_consumption_co2 = {}
        self.phev10_gasoline_consumption = {}
        self.phev10_gasoline_consumption_mmbtu = {}
        self.phev10_gasoline_consumption_co2 = {}
        self.phev20_gasoline_consumption = {}
        self.phev20_gasoline_consumption_mmbtu = {}
        self.phev20_gasoline_consumption_co2 = {}
        self.phev40_gasoline_consumption = {}
        self.phev40_gasoline_consumption_mmbtu = {}
        self.phev40_gasoline_consumption_co2 = {}
        self.bev100_gasoline_consumption = {}
        self.bev100_gasoline_consumption_mmbtu = {}
        self.bev100_gasoline_consumption_co2 = {}
        self.ice_gasoline_consumption = {}
        self.ice_gasoline_consumption_mmbtu = {}
        self.ice_gasoline_consumption_co2 = {}
        self.ev_share = {}

        self.bev100_population = {}
        self.phev10_population = {}
        self.phev20_population = {}
        self.phev40_population = {}
        self.phev_population = {}
        self.bev100_vmt = {}
        self.phev10_vmt = {}
        self.phev20_vmt = {}
        self.phev40_vmt = {}
        self.bev100_replacements, self.bev100_new_sales, self.bev100_sales = ({}, {}, {})
        self.phev10_replacements, self.phev10_new_sales, self.phev10_sales = ({}, {}, {})
        self.phev20_replacements, self.phev20_new_sales, self.phev20_sales = ({}, {}, {})
        self.phev40_replacements, self.phev40_new_sales, self.phev40_sales = ({}, {}, {})
        self.phev_replacements, self.phev_new_sales, self.phev_sales = ({}, {}, {})

    def process_annual_data(self, annual_data):
        first_row = True

        for row in annual_data:

            if first_row:
                first_row = False
                pass
            else:
                year = int(row[0])
                population = float(row[1])
                total_population = float(row[2])
                new_vmt = float(row[3])
                inc_price = float(row[4])
                new_mpg = float(row[5])
                bev100_population = float(row[6])
                phev10_population = float(row[7])
                phev20_population = float(row[8])
                phev40_population = float(row[9])
                bev100_vmt = float(row[10])
                phev10_vmt = float(row[11])
                phev20_vmt = float(row[12])
                phev40_vmt = float(row[13])

                self.population[year] = population
                self.total_population[year] = total_population
                self.inc_prices[year] = inc_price
                self.new_mpg[year] = new_mpg
                self.new_vmt[year] = new_vmt

                self.bev100_population[year] = bev100_population
                self.phev10_population[year] = phev10_population
                self.phev20_population[year] = phev20_population
                self.phev40_population[year] = phev40_population
                self.bev100_vmt[year] = bev100_vmt
                self.phev10_vmt[year] = phev10_vmt
                self.phev20_vmt[year] = phev20_vmt
                self.phev40_vmt[year] = phev40_vmt
                self.phev_population[year] = phev10_population + phev20_population + phev40_population


    def process_gasprices(self, gasprice_data):
        first_row = True

        for row in gasprice_data:

            if first_row:
                first_row = False
                pass
            else:
                year = int(row[0])
                gas_price = float(row[1])
                self.gas_prices[year] = gas_price

    def create_adoption_data(self, vehicle_lifetime):

        adoption_years = sorted(self.population.keys())
        adoption_start = min(adoption_years)
        adoption_end = max(adoption_years)

        self.new_sales[adoption_start] = self.population[adoption_start]
        self.ldv_new_sales[adoption_start] = self.total_population[adoption_start]
        self.vehicle_lifetime = vehicle_lifetime

        for year in range(adoption_start + 1, adoption_end + 1):
            self.new_sales[year] = self.population[year] - self.population[year-1]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.new_sales[year] = 0.

        first_replacement_year = adoption_start + vehicle_lifetime
        for year in range(adoption_start, first_replacement_year):
            self.replacements[year] = 0.

        for year in range(first_replacement_year, adoption_end + 1):
            self.replacements[year] = \
                self.new_sales[year - vehicle_lifetime] + self.replacements[year - vehicle_lifetime]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.replacements[year] = 0.

        for year in range(adoption_start, adoption_end + vehicle_lifetime):
            self.sales[year] = self.new_sales[year] + self.replacements[year]

        # Adoption data for Total LDV Population

        for year in range(adoption_start + 1, adoption_end + 1):
            self.ldv_new_sales[year] = self.total_population[year] - self.total_population[year-1]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.ldv_new_sales[year] = 0.

        first_replacement_year = adoption_start + vehicle_lifetime
        for year in range(adoption_start, first_replacement_year):
            self.ldv_replacements[year] = 0.

        for year in range(first_replacement_year, adoption_end + 1):
            self.ldv_replacements[year] = \
                self.ldv_new_sales[year - vehicle_lifetime] + self.ldv_replacements[year - vehicle_lifetime]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.ldv_replacements[year] = 0.

        for year in range(adoption_start, adoption_end + vehicle_lifetime):
            self.ldv_sales[year] = self.ldv_new_sales[year] + self.ldv_replacements[year]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.population[year] = self.population[year-1] - self.sales[year - vehicle_lifetime]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            self.total_population[year] = self.total_population[year - 1] - self.ldv_sales[year - vehicle_lifetime]

        self.bev100_population, self.bev100_new_sales, self.bev100_replacements, self.bev100_sales = \
            self.stock_rollover(adoption_start, adoption_end, vehicle_lifetime,  self.bev100_population)

        self.phev10_population, self.phev10_new_sales, self.phev10_replacements, self.phev10_sales = \
            self.stock_rollover(adoption_start, adoption_end, vehicle_lifetime, self.phev10_population)

        self.phev20_population, self.phev20_new_sales, self.phev20_replacements, self.phev20_sales = \
            self.stock_rollover(adoption_start, adoption_end, vehicle_lifetime, self.phev20_population)

        self.phev40_population, self.phev40_new_sales, self.phev40_replacements, self.phev40_sales = \
            self.stock_rollover(adoption_start, adoption_end, vehicle_lifetime, self.phev40_population)

        self.phev_population, self.phev_new_sales, self.phev_replacements, self.phev_sales = \
            self.stock_rollover(adoption_start, adoption_end, vehicle_lifetime, self.phev_population)

        self.adoption_years = adoption_years
        self.first_replacement_year = min(year for year in list(self.replacements.keys()) if self.replacements[year] > 0)

    def get_capital_cost(self, model_years):

        for year in model_years:
            if year in self.adoption_years:
                inc_price = self.inc_prices[year]
                sales = self.sales[year]
                cost = inc_price*sales
                self.capital_cost[year] = cost
            else:
                self.capital_cost[year] = 0.0

    def stock_rollover(self, adoption_start, adoption_end, vehicle_lifetime, population):
        new_sales = {}
        replacements = {}
        sales = {}

        new_sales[adoption_start] = population[adoption_start]

        for year in range(adoption_start + 1, adoption_end + 1):
            new_sales[year] = population[year] - population[year-1]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            new_sales[year] = 0.

        first_replacement_year = adoption_start + vehicle_lifetime
        for year in range(adoption_start, first_replacement_year):
            replacements[year] = 0.

        for year in range(first_replacement_year, adoption_end + 1):
            replacements[year] = \
                new_sales[year - vehicle_lifetime] + replacements[year - vehicle_lifetime]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            replacements[year] = 0.

        for year in range(adoption_start, adoption_end + vehicle_lifetime):
            sales[year] = new_sales[year] + replacements[year]

        for year in range(adoption_end + 1, adoption_end + vehicle_lifetime):
            population[year] = population[year-1] - sales[year - vehicle_lifetime]

        return population, new_sales, replacements, sales


    def get_tax_credit(self, model_years, last_taxcredit_year, tax_credit_bev, tax_credit_phev, credit_to_replacements):

        for year in model_years:
            if year <= last_taxcredit_year:
                if credit_to_replacements:
                    self.tax_credit[year] = self.bev100_sales[year]*tax_credit_bev[year]
                    self.tax_credit[year] += self.phev_sales[year] * tax_credit_phev[year]
                else:
                    self.tax_credit[year] = self.bev_new_sales[year] * tax_credit_bev[year]
                    self.tax_credit[year] = self.phev_new_sales[year]*tax_credit_phev[year]
            else:
                self.tax_credit[year] = 0.0


    def get_oandm_savings(self, model_years, bev_annual_oandm_savings, phev_annual_oandm_savings):

        start_year = min(model_years)

        for year in model_years:

            # If there are still old cars on the road, only cars adopted in model years
            if year < start_year + self.vehicle_lifetime:
                eligible_vehicles = sum(self.bev100_sales[y] for y in range(start_year, year + 1))
                self.bev_oandm_savings[year] = eligible_vehicles*bev_annual_oandm_savings
            # Otherwise the whole population
            else:
                self.bev_oandm_savings[year] = self.bev100_population[year] * bev_annual_oandm_savings

            if year < start_year + self.vehicle_lifetime:
                eligible_vehicles = sum(self.phev_sales[y] for y in range(start_year, year + 1))
                self.phev_oandm_savings[year] = eligible_vehicles*phev_annual_oandm_savings
            # Otherwise the whole population
            else:
                self.phev_oandm_savings[year] = self.phev_population[year] * phev_annual_oandm_savings

            self.oandm_savings[year] = self.phev_oandm_savings[year] + self.bev_oandm_savings[year]


    def get_gasoline_savings(self, model_years, metrictons_per_gallon, nox_emis, pm10_emis, so2_emis, voc_emis):

        bev100_gallons_avoided, bev100_co2_savings, bev100_nox_savings, bev100_pm10_savings, bev100_so2_savings, bev100_voc_savings, bev100_gasoline_savings = self.gasoline_avoided(
            model_years, self.bev100_population, self.bev100_sales, self.bev100_replacements,
            self.bev100_vmt, metrictons_per_gallon, nox_emis, pm10_emis, so2_emis, voc_emis)

        phev10_gallons_avoided, phev10_co2_savings, phev10_nox_savings, phev10_pm10_savings, phev10_so2_savings, phev10_voc_savings, phev10_gasoline_savings = self.gasoline_avoided(
            model_years, self.phev10_population, self.phev10_sales, self.phev10_replacements,
            self.phev10_vmt, metrictons_per_gallon, nox_emis, pm10_emis, so2_emis, voc_emis)

        phev20_gallons_avoided, phev20_co2_savings, phev20_nox_savings, phev20_pm10_savings, phev20_so2_savings, phev20_voc_savings, phev20_gasoline_savings = self.gasoline_avoided(
            model_years, self.phev20_population, self.phev20_sales, self.phev20_replacements,
            self.phev20_vmt, metrictons_per_gallon, nox_emis, pm10_emis, so2_emis, voc_emis)

        phev40_gallons_avoided, phev40_co2_savings, phev40_nox_savings, phev40_pm10_savings, phev40_so2_savings, phev40_voc_savings, phev40_gasoline_savings = self.gasoline_avoided(
            model_years, self.phev40_population, self.phev40_sales, self.phev40_replacements,
            self.phev40_vmt, metrictons_per_gallon, nox_emis, pm10_emis, so2_emis, voc_emis)

        self.gallons_avoided = (helpers.dsum(bev100_gallons_avoided, phev10_gallons_avoided,
                                             phev20_gallons_avoided, phev40_gallons_avoided))
        self.co2_savings = (helpers.dsum(bev100_co2_savings, phev10_co2_savings,
                                         phev20_co2_savings, phev40_co2_savings))
        self.nox_savings = (helpers.dsum(bev100_nox_savings, phev10_nox_savings,
                                         phev20_nox_savings, phev40_nox_savings))
        self.pm10_savings = (helpers.dsum(bev100_pm10_savings, phev10_pm10_savings,
                                          phev20_pm10_savings, phev40_pm10_savings))
        self.so2_savings = (helpers.dsum(bev100_so2_savings, phev10_so2_savings,
                                         phev20_so2_savings, phev40_so2_savings))
        self.voc_savings = (helpers.dsum(bev100_voc_savings, phev10_voc_savings,
                                         phev20_voc_savings, phev40_voc_savings))


        self.gasoline_savings = (helpers.dsum(bev100_gasoline_savings, phev10_gasoline_savings,
                                              phev20_gasoline_savings, phev40_gasoline_savings))

    def gasoline_avoided(self, model_years, population, sales_dict, replacements, vmt, co2_metrictons_per_gallon,
                         nox_emis, pm10_emis, so2_emis, voc_emis):

        mpg_improvement_factors = {}
        vmt_change_factor = {}
        gallons_avoided_dict = {}
        co2_savings = {}
        nox_savings = {}
        pm_10_savings = {}
        so2_savings = {}
        voc_savings = {}
        gasoline_savings = {}
        start_year = min(model_years)
        original_mpg = self.new_mpg[start_year]

        original_vmt = vmt[start_year]
        first_allreplacement_year = start_year + self.vehicle_lifetime

        gallons_per_ice = old_div(vmt[start_year], self.new_mpg[start_year])

        for year in range(start_year, max(model_years) + 1):

            if year >= start_year:
                if year <= max(self.adoption_years):
                    current_mpg = self.new_mpg[year]
                    current_vmt = vmt[year]
                    try:
                        mpg_improvement_factors[year] = old_div(original_mpg, current_mpg)
                        vmt_change_factor[year] = old_div(current_vmt, original_vmt)
                    except:
                        mpg_improvement_factors[year] = 0.
                        vmt_change_factor[year] = 0.

                else:
                    mpg_improvement_factors[year] = 0.
                    vmt_change_factor[year] = 0.

        for year in model_years:
            if year == start_year:
                gallons_avoided = old_div(population[year] * original_vmt, original_mpg)

            elif year < first_allreplacement_year:
                sales = [sales_dict[y] for y in range(year, start_year, -1)]
                factors = [vmt_change_factor[y] * mpg_improvement_factors[y]
                           for y in range(year, start_year, -1)]
                weighted_population = sum(sales[i]*factors[i] for i in range(len(sales)))
                replacement_gallons_avoided = weighted_population * gallons_per_ice

                all_replacements = sum(replacements[y] for y in range(year, start_year, -1))
                nonreplacement_vehicles = population[start_year] - all_replacements
                nonreplacement_gallons_avoided = \
                    nonreplacement_vehicles * gallons_per_ice * vmt_change_factor[start_year] *\
                    mpg_improvement_factors[start_year]
                gallons_avoided = replacement_gallons_avoided + nonreplacement_gallons_avoided

            else:
                sales = [sales_dict[y] for y in range(year, year - self.vehicle_lifetime, -1)]
                factors = [vmt_change_factor[y] * mpg_improvement_factors[y] for y in range(
                    year, year - self.vehicle_lifetime, -1)]
                weighted_population = sum(sales[i]*factors[i] for i in range(len(sales)))
                gallons_avoided = weighted_population * gallons_per_ice

            gallons_avoided_dict[year] = gallons_avoided
            co2_savings[year] = co2_metrictons_per_gallon*gallons_avoided
            nox_savings[year] = gallons_avoided * nox_emis
            pm_10_savings[year] = gallons_avoided * pm10_emis
            so2_savings[year] = gallons_avoided * so2_emis
            voc_savings[year] = gallons_avoided * voc_emis
            gasoline_savings[year] = gallons_avoided * self.gas_prices[year]

        return gallons_avoided_dict, co2_savings, nox_savings, pm_10_savings, so2_savings, voc_savings, gasoline_savings

    def get_gasoline_consumption(self, model_years, base_gasoline_consumption, base_year, metrictons_per_gallon,
                                 end_year, ice_vmt, phev10_vmt, phev20_vmt, phev40_vmt, bev100_vmt):
        """
        Input base year gasoline consumption, and escalate to future.
        Accounts for MPG improvements, VMT changes, and Total Vehicle population changes.
        """

        ice_population = {}
        ice_gas_consumption = {}
        population_escalation_factor = {}
        mile_escalation_factor = {}

        start_year = min(model_years)
        original_mpg = self.new_mpg[start_year]

        first_allreplacement_year = start_year + self.vehicle_lifetime

        gallons_per_ice = old_div(ice_vmt[start_year], self.new_mpg[start_year])
        gallons_per_phev10 = old_div((ice_vmt[start_year] - phev10_vmt[start_year]), self.new_mpg[start_year])
        gallons_per_phev20 = old_div((ice_vmt[start_year] - phev20_vmt[start_year]), self.new_mpg[start_year])
        gallons_per_phev40 = old_div((ice_vmt[start_year] - phev40_vmt[start_year]), self.new_mpg[start_year])
        gallons_per_bev100 = old_div((ice_vmt[start_year] - bev100_vmt[start_year]), self.new_mpg[start_year])

        max_year = max(self.total_population.keys())
        self.gas_consumption_range = list(range(base_year, max_year))


        for year in self.gas_consumption_range:
            try:
                mile_escalation_factor[year] = (old_div(ice_vmt[year],ice_vmt[start_year])) *\
                                               (old_div(self.new_mpg[start_year],self.new_mpg[year]))
            except:
                mile_escalation_factor[year] = 1

            ice_population[year] = self.total_population[year] - self.population[year]
            self.ice_gasoline_consumption[year] = ice_population[year] * mile_escalation_factor[year] * gallons_per_ice
            self.phev10_gasoline_consumption[year] = self.phev10_population[year] * mile_escalation_factor[
                year] * gallons_per_phev10
            self.phev20_gasoline_consumption[year] = self.phev20_population[year] * mile_escalation_factor[
                year] * gallons_per_phev20
            self.phev40_gasoline_consumption[year] = self.phev40_population[year] * mile_escalation_factor[
                year] * gallons_per_phev40
            self.bev100_gasoline_consumption[year] = self.bev100_population[year] * mile_escalation_factor[
                year] * gallons_per_bev100

            self.ice_gasoline_consumption_mmbtu[year] = self.ice_gasoline_consumption[year] * constants.MMBTU_per_gal
            self.phev10_gasoline_consumption_mmbtu[year] = self.phev10_gasoline_consumption[
                                                               year] * constants.MMBTU_per_gal
            self.phev20_gasoline_consumption_mmbtu[year] = self.phev20_gasoline_consumption[
                                                               year] * constants.MMBTU_per_gal
            self.phev40_gasoline_consumption_mmbtu[year] = self.phev40_gasoline_consumption[
                                                               year] * constants.MMBTU_per_gal
            self.bev100_gasoline_consumption_mmbtu[year] = self.bev100_gasoline_consumption[
                                                               year] * constants.MMBTU_per_gal

            self.ice_gasoline_consumption_co2[year] = self.ice_gasoline_consumption[year] * metrictons_per_gallon
            self.phev10_gasoline_consumption_co2[year] = self.phev10_gasoline_consumption[
                                                               year] * metrictons_per_gallon
            self.phev20_gasoline_consumption_co2[year] = self.phev20_gasoline_consumption[
                                                               year] * metrictons_per_gallon
            self.phev40_gasoline_consumption_co2[year] = self.phev40_gasoline_consumption[
                                                               year] * metrictons_per_gallon
            self.bev100_gasoline_consumption_co2[year] = self.bev100_gasoline_consumption[
                                                               year] * metrictons_per_gallon

            population_escalation_factor[year] = old_div(ice_population[year], self.total_population[base_year])

            self.gasoline_consumption[year] =\
                base_gasoline_consumption * population_escalation_factor[year] * 1e6 * mile_escalation_factor[year]
            self.gasoline_consumption_mmbtu[year] = \
                base_gasoline_consumption * population_escalation_factor[year] * 1e6 * mile_escalation_factor[year]\
                * constants.MMBTU_per_gal
            self.gasoline_consumption_co2[year] = base_gasoline_consumption * population_escalation_factor[year] *\
                                                  1e6 * mile_escalation_factor[year] * metrictons_per_gallon
            try:
                self.ev_share[year] = 1-(old_div(ice_population[year], self.total_population[year]))
            except:
                self.ev_share[year] = 1-(old_div(ice_population[end_year], self.total_population[end_year]))


        self.gasoline_consumption = dict(Counter(self.ice_gasoline_consumption) + Counter(self.phev10_gasoline_consumption) +
             Counter(self.phev20_gasoline_consumption) + Counter(self.phev40_gasoline_consumption) +
                                         Counter(self.bev100_gasoline_consumption))

        self.gasoline_consumption_mmbtu = dict(Counter(self.ice_gasoline_consumption_mmbtu) + Counter(self.phev10_gasoline_consumption_mmbtu) +
             Counter(self.phev20_gasoline_consumption_mmbtu) + Counter(self.phev40_gasoline_consumption_mmbtu) +
                                         Counter(self.bev100_gasoline_consumption_mmbtu))

        self.gasoline_consumption_co2 = dict(Counter(self.ice_gasoline_consumption_co2) + Counter(self.phev10_gasoline_consumption_co2) +
             Counter(self.phev20_gasoline_consumption_co2) + Counter(self.phev40_gasoline_consumption_co2) +
                                         Counter(self.bev100_gasoline_consumption_co2))

