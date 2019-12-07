from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from script.models.data import County
from script.models.statistics import Energy

def create_county(county_name, total_session, total_energy, peak_energy):
    client = APIClient()
    url = reverse('county-list')
    data = {
        'name': county_name,
        'total_session': total_session,
        'total_energy': total_energy,
        'peak_energy': peak_energy
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


def create_load_forecast(aggregation_level,
                        num_evs,
                        choice,
                        fast_percent,
                        work_percent,
                        res_percent,
                        l1_percent,
                        public_l2_percent,
                        residential_l1_load,
                        residential_l2_load,
                        residential_mud_load,
                        work_load,
                        fast_load,
                        public_l2_load,
                        total_load):
    client = APIClient()
    url = reverse('algorithm/load_forecast-list')
    data = {
        'aggregation_level': aggregation_level.name,
        'num_evs': num_evs,
        'choice': choice,
        'fast_percent': fast_percent,
        'work_percent': work_percent,
        'res_percent': res_percent,
        'l1_percent': l1_percent,
        'public_l2_percent': public_l2_percent,
        'residential_l1_load': residential_l1_load,
        'residential_l2_load': residential_l2_load,
        'residential_mud_load': residential_mud_load,
        'work_load': work_load,
        'fast_load': fast_load,
        'public_l2_load': public_l2_load,
        'total_load': total_load
    }
    response = client.post(url, data, format='json')
    return response


def create_load_forecast_config(config_name,
                                aggregation_level,
                                num_evs,
                                choice,
                                fast_percent,
                                work_percent,
                                res_percent,
                                l1_percent,
                                public_l2_percent):
    client = APIClient()
    url = reverse('config/load_forecast-list')
    data = {
        'config_name': config_name,
        'aggregation_level': aggregation_level.name,
        'num_evs': num_evs,
        'choice': choice,
        'fast_percent': fast_percent,
        'work_percent': work_percent,
        'res_percent': res_percent,
        'l1_percent': l1_percent,
        'public_l2_percent': public_l2_percent
    }
    response = client.post(url, data, format='json')
    return response


def create_load_profile(config, poi, year, day_type, loads):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/load_profile-list')
    data = {
        'config': config.id,
        'poi': poi.name,
        'year': year,
        'day_type': day_type.name,
        'loads': loads
    }
    response = client.post(url, data, format='json')
    return response


def create_gas_consumption(config, year, consumption):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/gas_consumption-list')
    data = {
        'config': config.id,
        'year': year,
        'consumption': consumption
    }
    response = client.post(url, data, format='json')
    return response


def create_cost_benefit(config, year, cost_benefit):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/cost_benefit-list')
    data = {
        'config': config.id,
        'year': year,
        'cost_benefit': cost_benefit
    }
    response = client.post(url, data, format='json')
    return response


def create_net_present_value(config, year, npv):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/net_present_value-list')
    data = {
        'config': config.id,
        'year': year,
        'npv': npv
    }
    response = client.post(url, data, format='json')
    return response


def create_emission(config, year, emissions):
    client = APIClient()
    url = reverse('algorithm/cost_benefit_analysis/emission-list')
    data = {
        'config': config.id,
        'year': year,
        'emissions': emissions
    }
    response = client.post(url, data, format='json')
    return response
