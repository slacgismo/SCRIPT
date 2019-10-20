from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient
from script.models.data import County
from script.models.statistics import Energy

# Create your tests here.
# ref:
# (1) https://www.django-rest-framework.org/api-guide/testing/
# (2) https://www.django-rest-framework.org/api-guide/routers/#routing-for-extra-actions
# (3) https://docs.djangoproject.com/en/2.2/topics/db/examples/many_to_one/


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


class CountyTests(APITestCase):

    county_name = 'Santa Cruz'
    residents = 9812

    def test_create_county(self):
        """
        Ensure we can create a new county object.
        """
        response = create_county(self.county_name, self.residents)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(County.objects.count(), 1)
        obj = County.objects.get()
        self.assertEqual(obj.name, self.county_name)
        self.assertEqual(obj.residents, self.residents)


class EnergyTests(APITestCase):

    county_name = 'Santa Cruz'
    residents = 9812
    year = 2019
    month = 10
    energy = 1234.5

    def test_create_energy(self):
        """
        Ensure we can create a new energy object.
        """
        _ = create_county(self.county_name, self.residents)
        response = create_energy(self.county_name, self.year, self.month, self.energy)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Energy.objects.count(), 1)
        obj = Energy.objects.get()
        self.assertEqual(obj.county.name, self.county_name)
        self.assertEqual(obj.year, self.year)
        self.assertEqual(obj.month, self.month)

    def test_filter_county(self):
        """
        Ensure we can filter energies by fields: county, year, month.
        """
        _ = create_county(self.county_name, self.residents)
        response = create_energy(self.county_name, self.year, self.month, self.energy)
        response = create_energy(self.county_name, self.year, 11, self.energy)
        url = reverse('county-list')
        data = {
            'county': self.county_name,
            'year': self.year,
            'month': self.month
        }
        response = self.client.get(url, data)
        obj = Energy.objects.get(county=self.county_name, year=self.year, month=self.month)
        self.assertEqual(obj.county.name, self.county_name)
        self.assertEqual(obj.year, self.year)
        self.assertEqual(obj.month, self.month)
        self.assertEqual(obj.energy, self.energy)
