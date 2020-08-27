from rest_framework import viewsets, status, filters
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from projects.models import Project
from .serializers import ProjectSerializer, ProjectDetailSerializer, ProjectRegisterSerializer, ProjectUpdateSerializer


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    filterset_fields = search_fields
    http_method_names = ['get', 'post', 'put', 'patch', 'delete']

    def get_queryset(self):
        return Project.objects.all()

    def create(self, request):
        serializer = ProjectRegisterSerializer(
            data=request.data, context={'request': request, 'data': request.data}
        )
        response_message = None
        response_status = status.HTTP_201_CREATED
        if serializer.is_valid() and serializer.isValidNavers():
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
        project_queryset = Project.objects.get(id=pk)
        serializer = ProjectDetailSerializer(project_queryset)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        project_queryset = Project.objects.get(id=pk)
        serializer = ProjectUpdateSerializer(project_queryset, data=request.data, partial=True)
        response_message = None
        response_status = status.HTTP_200_OK
        if request.user == project_queryset.user:
            if serializer.is_valid():
                try:
                    serializer.save()
                    serializer.addProjects(project_queryset, request.data)
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
        project_queryset = Project.objects.get(id=pk)
        serializer = ProjectUpdateSerializer(project_queryset, data=request.data)
        response_message = None
        response_status = status.HTTP_200_OK
        if request.user == project_queryset.user:
            if serializer.is_valid():
                try:
                    serializer.save()
                    serializer.addProjects(project_queryset, request.data)
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

    def destroy(self, request, pk=None):
        project_queryset = Project.objects.get(id=pk)
        response_status = status.HTTP_200_OK
        response_message = {"Success": "Project successfully deleted"}
        if request.user == project_queryset.user:
            project_queryset.delete()
        else:
            response_message = {"Failed": "Action denied"}
            response_status = status.HTTP_401_UNAUTHORIZED
        return Response(data=response_message, status=response_status)

