from django.shortcuts import reverse

from rest_framework.test import APITestCase


# Create your tests here.
class TestProductApi(APITestCase):
    def test_product_url(self):
        url = reverse('product-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)