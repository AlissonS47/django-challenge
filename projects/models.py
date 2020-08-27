from django.db import models
from django.contrib.auth.models import User


class Project(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    navers = models.ManyToManyField(to='users.Naver')

    def __str__(self):
        return self.name
