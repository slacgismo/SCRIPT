from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from script.models.data import County
from script.tests.utils import create_county

import json
from pprint import pprint

class CountyTests(APITestCase):

    county_name = 'Santa Cruz'
    residents = 9812

    def test_create_county(self):
        """Ensure we can create a new county object."""
        response = create_county(self.county_name, self.residents)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(County.objects.count(), 1)
        obj = County.objects.get()
        self.assertEqual(obj.name, self.county_name)
        self.assertEqual(obj.residents, self.residents)

    def test_create_conflict(self):
        """Ensure we cannot create two counties with the same name."""
        _ = create_county(self.county_name, self.residents)
        response = create_county(self.county_name, self.residents + 1)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_list_counties(self):
        """Ensure we can list all counties."""
        _ = create_county(self.county_name, self.residents)
        _ = create_county('Sunnyvale', self.residents + 1)
        _ = create_county('Palo Alto', self.residents + 2)
        url = reverse('county-list')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = json.loads(response.content)
        self.assertEqual(len(data), 3)

    def test_delete_county(self):
        """Ensure we can delete a county by its primary key."""
        response = create_county(self.county_name, self.residents)
        data = json.loads(response.content)
        url = reverse('county-detail', args=[self.county_name])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_modify_county(self):
        """Ensure we can modify a county by its primary key."""
        _ = create_county(self.county_name, self.residents)
        url = reverse('county-detail', args=[self.county_name])
        data = {
            'name': self.county_name,
            'residents': self.residents + 1
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = self.client.get(url, format='json')
        data = json.loads(response.content)
        self.assertEqual(data['residents'], self.residents + 1)
