from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from script.models.data import County
from script.models.statistics import Energy

def create_county(county_name, residents):
    client = APIClient()
    url = reverse('county-list')
    data = {
        'name': county_name,
        'residents': residents
    }
    response = client.post(url, data, format='json')
    return response


def create_energy(county_name, year, month, energy):
    client = APIClient()
    url = reverse('energy-list')
    data = {
        'county': county_name,
        'year': year,
        'month': month,
        'energy': energy
    }
    response = client.post(url, data, format='json')
    return response


def create_load_controller(county_name,
                            rate_energy_peak,
                            rate_energy_partpeak,
                            rate_energy_offpeak,
                            rate_demand_peak,
                            rate_demand_partpeak,
                            rate_demand_overall,
                            uncontrolled_load,
                            controlled_load):
    client = APIClient()
    url = reverse('algorithm/load_controller-list')
    data = {
        'county': county_name,
        'rate_energy_peak': rate_energy_peak,
        'rate_energy_partpeak': rate_energy_partpeak,
        'rate_energy_offpeak': rate_energy_offpeak,
        'rate_demand_peak': rate_demand_peak,
        'rate_demand_partpeak': rate_demand_partpeak,
        'rate_demand_overall': rate_demand_overall,
        'uncontrolled_load': uncontrolled_load,
        'controlled_load': controlled_load
    }
    response = client.post(url, data, format='json')
    return response


def create_aggregate_load_profile(year, day_type, loads):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/aggregate_load-list')
    data = {
        'year': year,
        'day_type': day_type.name,
        'loads': loads
    }
    response = client.post(url, data, format='json')
    return response
