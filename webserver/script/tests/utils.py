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


def create_load_profile(poi, year, day_type, loads):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/load_profile-list')
    data = {
        'poi': poi.name,
        'year': year,
        'day_type': day_type.name,
        'loads': loads
    }
    response = client.post(url, data, format='json')
    return response


def create_gas_consumption(year, consumption):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/gas_consumption-list')
    data = {
        'year': year,
        'consumption': consumption
    }
    response = client.post(url, data, format='json')
    return response


def create_cost_benefit(year, cost_benefit):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/cost_benefit-list')
    data = {
        'year': year,
        'cost_benefit': cost_benefit
    }
    response = client.post(url, data, format='json')
    return response


def create_net_present_value(year, npv):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/net_present_value-list')
    data = {
        'year': year,
        'npv': npv
    }
    response = client.post(url, data, format='json')
    return response
