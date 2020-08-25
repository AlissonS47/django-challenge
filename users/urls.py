from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from users.api.viewsets import UserRegisterViewSet, NaverViewSet


router = routers.DefaultRouter()
router.register(r'users/register', UserRegisterViewSet, basename='UserRegister')
router.register(r'navers', NaverViewSet, basename='Naver')

urlpatterns = [
    path('', include(router.urls)),
    path('users/login/', TokenObtainPairView.as_view()),
    path('users/login/refresh/', TokenRefreshView.as_view())
]
