from rest_framework import serializers
from django.contrib.auth.models import User


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