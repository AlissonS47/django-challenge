from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer

class UserRegisterViewSet(viewsets.ModelViewSet):

    queryset = User.objects.all()
    serializer_class = UserRegisterSerializer

    def create(self, request):
        user = UserRegisterSerializer(data=request.data)
        response_status = status.HTTP_201_CREATED
        if user.is_valid():
            try:
                user.save()
            except:
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Response(status=response_status)