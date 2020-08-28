import json
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.test import APITestCase
from .models import Naver
from projects.models import Project


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


class NaverTestCase(APITestCase):
    user_token = None
    user2 = None
    user2_token = None
    project_id = None

    def setUp(self):
        # primary user
        self.user = User.objects.create_user(username="test@django.com", password="strong_password")
        data = {"username": "test@django.com", "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.user_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')

        # secondary user
        self.user2 = User.objects.create_user(username="test2@django.com", password="strong_password")
        data = {"username": "test2@django.com", "password": "strong_password"}
        response = self.client.post('/users/login/', data)
        self.user2_token = response.data['access']

        # test project
        project = Project.objects.create(user=self.user, name='testproject')
        project.save()
        project = Project.objects.first()
        self.project_id = project.id

    def testRegistration(self):
        data = {
            "name": "testnaver",
            "birthdate": "2000-10-13",
            "job_role": "test",
            "projects": [self.project_id]
        }
        response = self.client.post('/navers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Naver.objects.get(name='testnaver'))
    
    def createNaver(self):
        # creates a naver and return he's id for use with the HTTP methods
        self.testRegistration()
        naver = self.client.get('/navers/')
        naver_id = dict(naver.data[0])['id']
        return naver_id
    
    def testRetrieve(self):
        naver_id = self.createNaver()
        response = self.client.get(f'/navers/{naver_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(dict(response.data)['name'], 'testnaver')

    def testUpdate(self):
        # create naver
        naver_id = self.createNaver()

        # data for update
        data = {
            "name": "testnaver.update",
            "birthdate": "1995-04-09",
            "job_role": "test update",
            "projects": []
        }

        # data for partial update
        partial_data = {
            "name": "partial_update"
        }

        # secondary user trying to update naver from primary user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.put(f'/navers/{naver_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Naver.objects.filter(name='testnaver.update').exists())
        
        # secondary user trying to partial update naver from primary user
        response = self.client.patch(f'/navers/{naver_id}/', partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Naver.objects.filter(name='partial_update').exists())

        # after update
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.put(f'/navers/{naver_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Naver.objects.filter(name='testnaver.update').exists())
        
        # after partial update
        response = self.client.patch(f'/navers/{naver_id}/', partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Naver.objects.filter(name='partial_update').exists())

    def testDelete(self):
        # create naver
        naver_id = self.createNaver()

        # before delete
        self.assertTrue(Naver.objects.filter(name='testnaver').exists())

        # secondary user trying to delete naver from primary user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.delete(f'/navers/{naver_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Naver.objects.filter(name='testnaver').exists())

        # after delete
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(f'/navers/{naver_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Naver.objects.filter(name='testnaver').exists())

    def testFilter(self):
        # create naver
        self.testRegistration()

        # whitout search
        response = self.client.get(
            '/navers/?name=testnaver&job_role=test&admission_date=2020-08-28'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        
        # with search
        response = self.client.get(
            '/navers/?search=naver'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)