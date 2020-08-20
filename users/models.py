from django.db import models
from django.contrib.auth.models import User


class Naver(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    birthdate = models.DateField()
    admission_date = models.DateField(auto_now_add=True)
    job_role = models.CharField(max_length=20)
    #projects

    def __str__(self):
        return self.name