from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from script.models.enums import DayType, POI
from script.models.data import County
from script.models.algorithms import LoadController, LoadProfile, GasConsumption
from script.tests.utils import create_county, create_load_controller, create_load_profile, create_gas_consumption

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
    year = 2020
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
        'BEV_100_Gasoline_Emissions_CO2': 570.7148746
    }

    def test_create_gas_consumption(self):
        """Ensure we can create a new gas consumption object."""
        response = create_gas_consumption(self.year, json.dumps(self.consumption))
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(GasConsumption.objects.count(), 1)
        obj = GasConsumption.objects.get()
        self.assertEqual(obj.year, self.year)
        self.assertEqual(json.loads(obj.consumption), self.consumption)
