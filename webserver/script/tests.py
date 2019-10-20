from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from script.models.data import County

# Create your tests here.

class CountyTests(APITestCase):
    def test_create_county(self):
        """
        Ensure we can create a new county object.
        """
        url = reverse('county-list')
        residents = 9812
        data = {
            'name': 'Santa Cruz',
            'residents': residents
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(County.objects.count(), 1)
        obj = County.objects.get()
        self.assertEqual(obj.name, 'Santa Cruz')
        self.assertEqual(obj.residents, residents)
