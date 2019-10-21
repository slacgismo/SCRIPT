from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from script.models.data import County
from script.tests.utils import create_county

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
