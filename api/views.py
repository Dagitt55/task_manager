from django.shortcuts import render

from rest_framework import viewsets, status  # Importing necessary classes for viewsets and HTTP status codes
from rest_framework.decorators import action  # Importing action decorator for custom actions
from rest_framework.response import Response  # Importing Response class to return API responses
from django.contrib.auth.models import User  # Importing User model for user management
from .models import Task  # Importing Task model from the current app
from .serializers import UserSerializer, TaskSerializer  # Importing serializers for User and Task
from rest_framework.permissions import IsAuthenticated, AllowAny  # Importing permission classes
from .permissions import IsOwner  # Importing custom permission class to check task ownership
from rest_framework_simplejwt.views import TokenObtainPairView  # Importing JWT token view for authentication

# ViewSet for managing User objects
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()  # Queryset to retrieve all users
    serializer_class = UserSerializer  # Specifying the serializer to use for User objects

    def get_permissions(self):
        # Setting permissions based on the action being performed
        if self.action in ['create']:
            return [AllowAny()]  # Allow any user to create a new account
        return [IsAuthenticated()]  # All other actions require authentication

# ViewSet for managing Task objects
class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer  # Specifying the serializer to use for Task objects
    permission_classes = [IsAuthenticated, IsOwner]  # Requiring authentication and ownership permissions
    filterset_fields = ['status', 'priority', 'due_date']  # Fields to filter tasks
    ordering_fields = ['due_date', 'priority']  # Fields to allow ordering of tasks

    def get_queryset(self):
        # Retrieving only tasks that belong to the authenticated user
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Saving the new task with the authenticated user as the owner
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        # Custom action to mark a task as complete
        task = self.get_object()  # Getting the task object based on the primary key
        if task.status == 'Completed':
            return Response({'detail': 'Task is already completed.'}, status=status.HTTP_400_BAD_REQUEST)  # Return error if already completed
        task.mark_completed()  # Mark the task as completed
        serializer = self.get_serializer(task)  # Serialize the updated task
        return Response(serializer.data)  # Return the serialized task data

    @action(detail=True, methods=['post'])
    def mark_incomplete(self, request, pk=None):
        # Custom action to mark a task as incomplete
        task = self.get_object()  # Getting the task object based on the primary key
        if task.status == 'Pending':
            return Response({'detail': 'Task is already pending.'}, status=status.HTTP_400_BAD_REQUEST)  # Return error if already pending
        task.mark_incomplete()  # Mark the task as incomplete
        serializer = self.get_serializer(task)  # Serialize the updated task
        return Response(serializer.data)  # Return the serialized task data

