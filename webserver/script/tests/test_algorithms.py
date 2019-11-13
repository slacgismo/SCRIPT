from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from script.models.enums import DayType, POI
from script.models.data import County
from script.models.algorithms import LoadController, LoadProfile, GasConsumption, CostBenefit, NetPresentValue
from script.tests.utils import create_county, create_load_controller, create_load_profile, create_gas_consumption, create_cost_benefit, create_net_present_value

import json
import copy

class LoadControllerTests(APITestCase):

    county_name = 'Santa Cruz'
    residents = 9812
    rate_energy_peak = 0.16997
    rate_energy_partpeak = 0.12236
    rate_energy_offpeak = 0.09082
    rate_demand_peak = 21.23
    rate_demand_partpeak = 5.85
    rate_demand_overall = 19.10
    uncontrolled_load = [
        {
            'time': '05:30',
            'load': '134'
        },
        {
            'time': '05:45',
            'load': '323'
        },
        {
            'time': '06:00',
            'load': '413'
        }
    ]
    controlled_load = [
        {
            'time': '05:30',
            'load': '130'
        },
        {
            'time': '05:45',
            'load': '320'
        },
        {
            'time': '06:00',
            'load': '410'
        }
    ]

    def test_create_load_controller(self):
        """Ensure we can create a new load controller object."""
        _ = create_county(self.county_name, self.residents)
        response = create_load_controller(self.county_name,
                                            self.rate_energy_peak,
                                            self.rate_energy_partpeak,
                                            self.rate_energy_offpeak,
                                            self.rate_demand_peak,
                                            self.rate_demand_partpeak,
                                            self.rate_demand_overall,
                                            json.dumps(self.uncontrolled_load),
                                            json.dumps(self.controlled_load))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoadController.objects.count(), 1)
        obj = LoadController.objects.get()
        self.assertEqual(obj.county.name, self.county_name)
        self.assertEqual(json.loads(obj.uncontrolled_load), self.uncontrolled_load)
        self.assertEqual(json.loads(obj.controlled_load), self.controlled_load)

    def test_create_conflict(self):
        """Ensure we cannot create two load controllers with the unique set."""
        _ = create_county(self.county_name, self.residents)
        _ = create_load_controller(self.county_name,
                                    self.rate_energy_peak,
                                    self.rate_energy_partpeak,
                                    self.rate_energy_offpeak,
                                    self.rate_demand_peak,
                                    self.rate_demand_partpeak,
                                    self.rate_demand_overall,
                                    json.dumps(self.uncontrolled_load),
                                    json.dumps(self.controlled_load))
        response = create_load_controller(self.county_name,
                                            self.rate_energy_peak,
                                            self.rate_energy_partpeak,
                                            self.rate_energy_offpeak,
                                            self.rate_demand_peak,
                                            self.rate_demand_partpeak,
                                            self.rate_demand_overall,
                                            json.dumps(self.uncontrolled_load),
                                            json.dumps(self.controlled_load))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_filter_county(self):
        """Ensure we can filter load controllers by fields: county, rates."""
        _ = create_county(self.county_name, self.residents)
        _ = create_load_controller(self.county_name,
                                    self.rate_energy_peak,
                                    self.rate_energy_partpeak,
                                    self.rate_energy_offpeak,
                                    self.rate_demand_peak,
                                    self.rate_demand_partpeak,
                                    self.rate_demand_overall,
                                    json.dumps(self.uncontrolled_load),
                                    json.dumps(self.controlled_load))
        new_controlled_load = copy.copy(self.controlled_load)
        new_controlled_load[0]['load'] = '110'
        response = create_load_controller(self.county_name,
                                            self.rate_energy_peak + 1,
                                            self.rate_energy_partpeak + 2,
                                            self.rate_energy_offpeak + 3,
                                            self.rate_demand_peak + 4,
                                            self.rate_demand_partpeak + 5,
                                            self.rate_demand_overall + 6,
                                            json.dumps(self.uncontrolled_load),
                                            json.dumps(new_controlled_load))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        url = reverse('algorithm/load_controller-list')
        data = {
            'county': self.county_name,
            'rate_energy_peak': self.rate_energy_peak + 1,
            'rate_energy_partpeak': self.rate_energy_partpeak + 2
        }
        response = self.client.get(url, data)
        obj = json.loads(response.content)[0]
        self.assertEqual(obj['county'], self.county_name)
        self.assertEqual(json.loads(obj['controlled_load']), new_controlled_load)


class LoadProfileTests(APITestCase):
    poi = POI.WORKPLACE
    year = 2020
    day_type = DayType.WEEKEND
    loads = [i * 2 % 24 + 1 for i in range(24)]

    def test_create_load_profile(self):
        """Ensure we can create a new load profile object."""
        response = create_load_profile(self.poi,
                                        self.year,
                                        self.day_type,
                                        json.dumps(self.loads))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(LoadProfile.objects.count(), 1)
        obj = LoadProfile.objects.get()
        self.assertEqual(obj.poi, self.poi.name)
        self.assertEqual(obj.year, self.year)
        self.assertEqual(obj.day_type, self.day_type.name)
        self.assertEqual(json.loads(obj.loads), self.loads)


class GasConsumptionTests(APITestCase):
    year = 2014
    consumption = {
        'Gasoline_Consumption_gallons': 545619941.6,
        'Gasoline_Consumption_MMBTU': 65734108089476.5,
        'Gasoline_Emissions_CO2': 4637769.504,
        'PHEV_10_Gasoline_Consumption_gallons': 24929.58517,
        'PHEV_10_Gasoline_Consumption_MMBTU': 3003416703,
        'PHEV_10_Gasoline_Emissions_CO2': 211.9014739,
        'PHEV_20_Gasoline_Consumption_gallons': 69108.54055,
        'PHEV_20_Gasoline_Consumption_MMBTU': 8325920531,
        'PHEV_20_Gasoline_Emissions_CO2': 587.4225947,
        'PHEV_40_Gasoline_Consumption_gallons': 95172.95918,
        'PHEV_40_Gasoline_Consumption_MMBTU': 11466057430,
        'PHEV_40_Gasoline_Emissions_CO2': 808.970153,
        'BEV_100_Gasoline_Consumption_gallons': 67142.92642,
        'BEV_100_Gasoline_Consumption_MMBTU': 8089111204,
        'BEV_100_Gasoline_Emissions_CO2': 570.7148746,
        'EV_Share': 0.001533283
    }

    def test_create_gas_consumption(self):
        """Ensure we can create a new gas consumption object."""
        response = create_gas_consumption(self.year, json.dumps(self.consumption))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GasConsumption.objects.count(), 1)
        obj = GasConsumption.objects.get()
        self.assertEqual(obj.year, self.year)
        self.assertEqual(json.loads(obj.consumption), self.consumption)


class CostBenefitTests(APITestCase):
    year = 2014
    cost_benefit = {
        'Utility_Bills': 1643285.189,
        'Utility_Bills_res': 1574878.503,
        'Utility_Bills_work': 27523.12322,
        'Utility_Bills_pub_L2': 40883.56269,
        'Utility_Bills_DCFC': 0,
        'Incremental_upfront_vehicle_cost': 15713196.73,
        'Charging_infrastructure_cost':	4573543.239,
        'Charging_infrastructure_cost_res':	2920300,
        'Charging_infrastructure_cost_work_L2':	632882.3529,
        'Charging_infrastructure_cost_public_L2': 430360,
        'Charging_infrastructure_cost_DCFC': 590000.8865,
        'Avoided_vehicle_gasoline ($)':	4604521.161,
        'Avoided_vehicle_gasoline (gallons)': 2029634.905,
        'Vehicle_O&M_Savings': 307236,
        'Federal_EV_Tax_Credit': 10166700,
        'Vehicle_sales': 1537,
        'Transmission_and_Distribution_Cost': 127854.8147,
        'Distribution_Cost': 87146.31329,
        'Transmission_Cost': 40708.50144,
        'Cumulative_personal_light-duty_EV_population':	6878,
        'Cumulative_personal_light-duty_LDV_population': 1293819,
        'EV_sales_as_percentage_of_total_personal_light-duty_vehicles':	0.001187956,
        'Peak_Demand_5-9_PM': 6.913490911,
        'Energy_Supply_Cost': 687051.7026,
        'Energy_Cost': 531222.3664,
        'Capacity_Cost': 155829.3361
    }

    def test_create_gas_consumption(self):
        """Ensure we can create a new cost benefit object."""
        response = create_cost_benefit(self.year, json.dumps(self.cost_benefit))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CostBenefit.objects.count(), 1)
        obj = CostBenefit.objects.get()
        self.assertEqual(obj.year, self.year)
        self.assertEqual(json.loads(obj.cost_benefit), self.cost_benefit)


class NetPresentValueTests(APITestCase):
    year = 2014
    net_present_value = {
        'Utility_Bills': 250514400.4,
        'Utility_Bills_volumetric':	250059210.3,
        'Utility_Bills_demand':	455190.0426,
        'Utility_Bills_res': 240325818.2,
        'Utility_Bills_work': 4088140.725,
        'Utility_Bills_pub_L2':	6100441.406,
        'Utility_Bills_DCFC': 0,
        'Incremental_upfront_vehicle_cost':	91394525.43,
        'Charging_infrastructure_cost': 324375153.1,
        'Charging_infrastructure_cost_res':	207241475.2,
        'Charging_infrastructure_cost_work_L2':	44902567.99,
        'Charging_infrastructure_cost_public_L2': 30533746.23,
        'Charging_infrastructure_cost_DCFC': 41697363.66,
        'Avoided_vehicle_gasoline':	802838445.2,
        'Vehicle_O&M_Savings': 207528684.2,
        'Federal_EV_Tax_Credit': 121338516.8,
        'Energy_Supply_Cost': 80844635.85,
        'Energy_Cost': 80844635.85,
        'Generation_Capacity_Cost':	23490407.75,
        'Vehicle_Sales': 132772.6619,
        'Transmission_and_Distribution_Cost': 15056754.47,
        'Distribution_Cost': 8905317.194,
        'Transmission_Cost': 6151437.278
    }

    def test_create_net_present_value(self):
        """Ensure we can create a new new present value object."""
        response = create_net_present_value(self.year, json.dumps(self.net_present_value))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(NetPresentValue.objects.count(), 1)
        obj = NetPresentValue.objects.get()
        self.assertEqual(obj.year, self.year)
        self.assertEqual(json.loads(obj.npv), self.net_present_value)
