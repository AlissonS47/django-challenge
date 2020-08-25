from django.db import models


class Project(models.Model):
    name = models.CharField(max_length=50)
    navers = models.ManyToManyField(to='users.Naver')

    def __str__(self):
        return self.name
