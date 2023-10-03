from budget.models import Category, Expense
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient


class ExpenseViewSetTestCase(APITestCase):
    def setUp(self):
        self.username = 'testuser'
        self.password = 'testpassword'
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.category = Category.objects.create(name='Category 1')
        self.expense = Expense.objects.create(category=self.category, amount=50)
        self.headers = {'Authorization': f'Token {self.get_auth_token(self.username, self.password)}'}

    def get_auth_token(self, username, password):
        client = APIClient()
        response = client.post('/api-token-auth/', {'username': username, 'password': password})
        self.assertEqual(response.status_code, 200)
        return response.data['token']

    def test_list_expenses(self):
        url = reverse('expense-list')
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_expense(self):
        data = {
            'category': self.category.pk,
            'amount': 75,
        }

        url = reverse('expense-list')
        response = self.client.post(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertEqual(Expense.objects.count(), 2)

    def test_retrieve_expense(self):
        url = reverse('expense-detail', args=[self.expense.id])
        response = self.client.get(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_expense(self):
        data = {
            'category': self.category.pk,
            'amount': 100,
        }

        url = reverse('expense-detail', args=[self.expense.id])
        response = self.client.put(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.expense.refresh_from_db()

        self.assertEqual(self.expense.amount, 100)

    def test_delete_expense(self):
        url = reverse('expense-detail', args=[self.expense.id])
        response = self.client.delete(url, headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        self.assertEqual(Expense.objects.count(), 0)