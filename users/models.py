from django.db import models
from django.contrib.auth.models import User
from projects.models import Project


class Naver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    birthdate = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    job_role = models.CharField(max_length=20)

    def __str__(self):
        return self.name

    @property
    def projects(self):
        return Project.objects.filter(navers=self.pk)
