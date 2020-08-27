from rest_framework import serializers
from projects.models import Project
from users.models import Naver


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['id', 'name']


class NaverSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Naver
        fields = ['id', 'name', 'birthdate', 'admission_date', 'job_role']
        

class ProjectDetailSerializer(serializers.ModelSerializer):
    navers = NaverSerializer(many=True)
    
    class Meta:
        model = Project
        fields = ['id', 'name', 'navers']


class ProjectRegisterSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['name']
    
    def isValidNavers(self):
        if 'navers' in self.context['data']:
            return True
        else:
            return False
    
    def addNavers(self, project, navers):
        for naver in navers:
            nv = Naver.objects.get(id=naver)
            project.navers.add(nv)

    def save(self):
        project = Project(
            user = self.context['request'].user,
            name = self.validated_data['name']
        )
        project.save()
        self.addNavers(project, self.context['data']['navers'])


class ProjectUpdateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = ['name']

    def addProjects(self, project, data):
        if 'navers' in data:
            for naver in project.navers.all():
                project.navers.remove(naver)

            for naver in data['navers']:
                nv = Naver.objects.get(id=naver)
                project.navers.add(nv)
        else:
            pass
