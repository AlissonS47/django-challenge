from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api.serializers import UserRegisterSerializer
from users.api.viewsets import UserRegisterViewSet


router = routers.DefaultRouter()
router.register(r'user/register/', UserRegisterViewSet, basename='UserRegister')

urlpatterns = [
    path('', include(router.urls)),
    path('user/login/', TokenObtainPairView.as_view()),
    path('user/login/refresh/', TokenRefreshView.as_view())
]
