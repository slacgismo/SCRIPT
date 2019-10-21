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
