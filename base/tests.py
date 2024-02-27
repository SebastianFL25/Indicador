from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from .models import CustomUser
from rest_framework_simplejwt.tokens import RefreshToken

class UsuarioCreateViewTest(APITestCase):
    def test_create_usuario(self):
        url = reverse('create')
        data = {'username': 'testuser', 'email': 'test@example.com', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())

class LoginViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')

    def test_login_valid_credentials(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'testpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_login_invalid_credentials(self):
        url = reverse('login')
        data = {'username': 'testuser', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RefreshViewTest(APITestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.refresh_token = RefreshToken.for_user(self.user)

    def test_refresh_valid_token(self):
        url = reverse('refresh')
        data = {'refresh': str(self.refresh_token)}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_refresh_invalid_token(self):
        url = reverse('refresh')
        data = {'refresh': 'invalid_token'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
