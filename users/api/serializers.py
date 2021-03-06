from rest_framework import serializers
from django.contrib.auth.models import User
from users.models import Naver
from projects.models import Project


class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['email', 'password']
    
    def save(self):
        user = User(
            username = self.validated_data['email'],
            email = self.validated_data['email']
        )
        user.set_password(self.validated_data['password'])
        user.save()


class NaverSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Naver
        fields = ['id', 'name', 'birthdate', 'admission_date', 'job_role']


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['id', 'name']


class NaverDetailSerializer(serializers.ModelSerializer):
    projects = ProjectSerializer(many=True)

    class Meta:
        model = Naver
        fields = ['id', 'name', 'birthdate', 'admission_date', 'job_role', 'projects']


class NaverRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Naver
        fields = ['name', 'birthdate', 'admission_date', 'job_role']
    
    def isValidProjects(self):
        if 'projects' in self.context['data']:
            return True
        else:
            return False
    
    def addProjects(self, naver, projects):
        for project in projects:
            pj = Project.objects.get(id=project)
            pj.navers.add(naver)
    

    def save(self):
        naver = Naver(
            user = self.context['request'].user,
            name = self.validated_data['name'],
            birthdate = self.validated_data['birthdate'],
            job_role = self.validated_data['job_role']
        )
        naver.save()
        self.addProjects(naver, self.context['data']['projects'])
        

class NaverUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Naver
        fields = ['name', 'birthdate', 'admission_date', 'job_role']

    def addProjects(self, project, data):
        if 'navers' in data:
            for naver in project.navers:
                nv = Naver.objects.get(id=project.id)
                project.navers.remove(nv)

            for project in data['projects']:
                pj = Project.objects.get(id=project)
                pj.navers.add(naver)
        else:
            pass


