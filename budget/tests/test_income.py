from budget.models import Category, Income
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class IncomeViewSetTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.category = Category.objects.create(name='Category 1')
        self.income = Income.objects.create(category=self.category, amount=100)
        self.headers = {'Authorization': f'Token {self.get_auth_token(self.username, self.password)}'}

    def get_auth_token(self, username, password):
        client = APIClient()
        response = client.post('/api-token-auth/', {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        return response.data['token']

    def test_list_incomes(self):
        url = reverse('income-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_income(self):
        data = {
            'category': self.category.pk,
            'amount': 200,
        }

        url = reverse('income-list')
        response = self.client.post(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Income.objects.count(), 2)

    def test_retrieve_income(self):
        url = reverse('income-detail', args=[self.income.id])
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_income(self):
        data = {
            'category': self.category.pk,
            'amount': 150,
        }

        url = reverse('income-detail', args=[self.income.id])
        response = self.client.put(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.income.refresh_from_db()

        self.assertEqual(self.income.amount, 150)

    def test_delete_income(self):
        url = reverse('income-detail', args=[self.income.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Income.objects.count(), 0)