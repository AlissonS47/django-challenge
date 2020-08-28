import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.test import APITestCase


class UserTestCase(APITestCase):
    user_data = None

    def setUp(self):
        self.user = User.objects.create_user(username="test@django.com", password="strong_password")
        self.user_data = {"username": "test@django.com", "password": "strong_password"}

    def testRegistration(self):
        data = {"email": "test.registration@django.com", "password": "strong_password"}
        response = self.client.post('/users/register/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.get(username='test.registration@django.com'))
    
    def testLogin(self):
        # testing with wrong username
        data = {"username": "wrong@django.com", "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # testing with wrong password
        data = {"username": "test@django.com", "password": "wrong_password"}
        response = self.client.post('/users/login/', data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # testing with correct username and password
        response = self.client.post('/users/login/', self.user_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def testLoginToken(self):
        response = self.client.post('/users/login/', self.user_data)
        self.assertTrue('refresh' in response.data)
        self.assertTrue('access' in response.data)
    
    def testLoginTokenRefresh(self):
        response = self.client.post('/users/login/', self.user_data)
        token_refresh = response.data['refresh']
        response = self.client.post('/users/login/refresh/', {"refresh": token_refresh})
        self.assertTrue('access' in response.data)
