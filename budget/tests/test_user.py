from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from budget.serializers import UserCreateSerializer


class UserCreateSerializerTestCase(APITestCase):
    def test_serializer_valid_data(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secure_password123'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_missing_required_fields(self):
        data = {
            'username': 'testuser'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_create_user(self):
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'secure_password123'
        }
        serializer = UserCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        user = serializer.save()
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(user.username, 'testuser')


class UserCreateViewTestCase(APITestCase):

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

    def test_create_user(self):
        url = reverse('create_user')
        data = {
            'username': 'testuser2',
            'email': 'test@example.com',
            'password': 'secure_password1234'
        }
        response = self.client.post(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)
        user = User.objects.last()
        self.assertEqual(user.username, 'testuser2')

    def test_create_user_missing_fields(self):
        url = reverse('create_user')
        data = {
            'username': 'testuser2'
        }
        response = self.client.post(url, data, format='json', headers=self.headers)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 1)