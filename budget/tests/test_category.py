from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from budget.models import Category
from budget.serializers import CategorySerializer


class CategoryViewSetTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.headers = {'Authorization': f'Token {self.get_auth_token(self.username, self.password)}'}

    def get_auth_token(self, username, password):
        client = APIClient()
        response = client.post('/api-token-auth/', {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        return response.data['token']

    def test_list_categories(self):
        Category.objects.create(name='Category 1')
        Category.objects.create(name='Category 2')

        url = reverse('category-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertEqual(len(response.data), 4)

    def test_create_category(self):
        data = {'name': 'New Category'}

        url = reverse('category-list')
        response = self.client.post(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Category.objects.count(), 1)

    def test_update_category(self):
        category = Category.objects.create(name='Old Name')
        data = {'name': 'New Name'}

        url = reverse('category-detail', args=[category.id])
        response = self.client.put(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        category.refresh_from_db()
        self.assertEqual(category.name, 'New Name')

    def test_delete_category(self):
        category = Category.objects.create(name='Category to Delete')

        url = reverse('category-detail', args=[category.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Category.objects.count(), 0)

class CategorySerializerTestCase(APITestCase):
    def test_valid_serializer_data(self):
        data = {'name': 'Valid Category'}
        serializer = CategorySerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_required_field(self):
        data = {}
        serializer = CategorySerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('name', serializer.errors)
