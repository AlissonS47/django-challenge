from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from users.models import Naver
from .models import Project


class ProjectTestCase(APITestCase):
    user_token = None
    user2 = None
    user2_token = None
    naver_id = None

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

        # test naver
        naver = Naver.objects.create(
            user=self.user, name='testnaver', birthdate='2020-08-28', job_role='test'
        )
        naver.save()
        naver = Naver.objects.first()
        self.naver_id = naver.id
    
    def testAuth(self):
        # without authentication
        self.client.credentials(HTTP_AUTHORIZATION='No Auth')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

        # with authentication
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.get('/projects/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def testRegistration(self):
        data = {
            "name": "testproject",
            "navers": [self.naver_id]
        }
        response = self.client.post('/projects/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Project.objects.get(name='testproject'))
    
    def createProject(self):
        # creates a project and return he's id for use with the HTTP methods
        self.testRegistration()
        project = self.client.get('/projects/')
        project_id = dict(project.data[0])['id']
        return project_id
    
    def testRetrieve(self):
        project_id = self.createProject()
        response = self.client.get(f'/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        self.assertEqual(dict(response.data)['name'], 'testproject')

    def testUpdate(self):
        # create project
        project_id = self.createProject()

        # data for update
        data = {
            "name": "testproject.update",
            "projects": []
        }

        # data for partial update
        partial_data = {
            "name": "partial_update"
        }

        # secondary user trying to update project from primary user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.put(f'/projects/{project_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Project.objects.filter(name='testproject.update').exists())
        
        # secondary user trying to partial update project from primary user
        response = self.client.patch(f'/projects/{project_id}/', partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertFalse(Project.objects.filter(name='partial_update').exists())

        # after update
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.put(f'/projects/{project_id}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Project.objects.filter(name='testproject.update').exists())
        
        # after partial update
        response = self.client.patch(f'/projects/{project_id}/', partial_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Project.objects.filter(name='partial_update').exists())

    def testDelete(self):
        # create project
        project_id = self.createProject()

        # before delete
        self.assertTrue(Project.objects.filter(name='testproject').exists())

        # secondary user trying to delete project from primary user
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user2_token}')
        response = self.client.delete(f'/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Project.objects.filter(name='testproject').exists())

        # after delete
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.user_token}')
        response = self.client.delete(f'/projects/{project_id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Project.objects.filter(name='testproject').exists())

    def testFilter(self):
        # create project
        self.testRegistration()

        # without search
        response = self.client.get('/projects/?name=testproject')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
        
        # with search
        response = self.client.get('/projects/?search=project')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)
