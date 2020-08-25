from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .serializers import UserRegisterSerializer, NaverSerializer, NaverDetailSerializer, NaverRegisterSerializer, NaverUpdateSerializer
from users.models import Naver


class UserRegisterViewSet(viewsets.ModelViewSet):

    serializer_class = UserRegisterSerializer
    http_method_names = ['post']

    def create(self, request):
        user = UserRegisterSerializer(data=request.data)
        response_status = status.HTTP_201_CREATED
        response_message = {"Success": "User successfully created"}
        if user.is_valid():
            try:
                user.save()
            except:
                response_message = {"Failed": "Internal server error"}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Failed": "Invalid data"}
            response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Response(data=response_message, status=response_status)


class NaverViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NaverSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'job_role', 'admission_date']
    filterset_fields = search_fields
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Naver.objects.all()

    def create(self, request):
        serializer = NaverRegisterSerializer(
            data=request.data, context={'request': request, 'data': request.data}
        )
        response_message = None
        response_status = status.HTTP_201_CREATED
        if serializer.is_valid() and serializer.isValidProjects():
            try:
                serializer.save()
                response_message = serializer.data
            except:
                response_message = {"Failed": "Internal server error"}
                response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            response_message = {"Failed": "Invalid data"}
            response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        return Response(data=response_message, status=response_status)

    def retrieve(self, request, pk=None):
        naver_queryset = Naver.objects.get(id=pk)
        serializer = NaverDetailSerializer(naver_queryset)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        naver_queryset = Naver.objects.get(id=pk)
        serializer = NaverUpdateSerializer(naver_queryset, data=request.data, partial=True)
        response_message = None
        response_status = status.HTTP_200_OK
        if request.user == naver_queryset.user:
            if serializer.is_valid():
                try:
                    serializer.save()
                    serializer.addProjects(naver_queryset, request.data)
                    response_message = serializer.data
                except:
                    response_message = {"Failed": "Internal server error"}
                    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                response_message = {"Failed": "Invalid data"}
                response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
        return Response(data=response_message, status=response_status)
    
    def update(self, request, pk=None):
        naver_queryset = Naver.objects.get(id=pk)
        serializer = NaverUpdateSerializer(naver_queryset, data=request.data)
        response_message = None
        response_status = status.HTTP_200_OK
        if request.user == naver_queryset.user:
            if serializer.is_valid():
                try:
                    serializer.save()
                    serializer.addProjects(naver_queryset, request.data)
                    response_message = serializer.data
                except:
                    response_message = {"Failed": "Internal server error"}
                    response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            else:
                response_message = {"Failed": "Invalid data"}
                response_status = status.HTTP_422_UNPROCESSABLE_ENTITY
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
        return Response(data=serializer.data, status=response_status)

    def destroy(self, request, pk=None):
        naver_queryset = Naver.objects.get(id=pk)
        response_status = status.HTTP_200_OK
        response_message = {"Success": "User successfully deleted"}
        if request.user == naver_queryset.user:
            naver_queryset.delete()
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
        return Response(data=response_message, status=response_status)

