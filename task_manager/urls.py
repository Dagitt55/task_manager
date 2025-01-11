"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  # Importing path and include for URL routing
from rest_framework import routers  # Importing routers for automatic URL routing with viewsets
from api.views import UserViewSet, TaskViewSet  # Importing viewsets for user and task management
from rest_framework_simplejwt.views import (
    TokenObtainPairView,  # View for obtaining a JWT token pair
    TokenRefreshView,  # View for refreshing a JWT token
)

# Creating a default router for registering viewsets
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)  # Registering the UserViewSet with the router
router.register(r'tasks', TaskViewSet, basename='task')  # Registering the TaskViewSet with the router

# Defining URL patterns for the application
urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the Django admin interface
    path('api/', include(router.urls)),  # Including the URLs from the router (users and tasks API endpoints)
    
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # URL for obtaining JWT token
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # URL for refreshing JWT token
]
