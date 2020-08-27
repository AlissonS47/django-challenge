from django.urls import path, include
from rest_framework import routers
from projects.api.viewsets import ProjectViewSet


router = routers.DefaultRouter()
router.register(r'projects', ProjectViewSet, basename='ProjectViewSet')

urlpatterns = [
    path('', include(router.urls)),
]
