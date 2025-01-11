from rest_framework import serializers  # Importing Django REST Framework's serializers
from django.contrib.auth.models import User  # Importing User model from Django's authentication system
from .models import Task  # Importing Task model from the current app's models
from django.utils import timezone  # Importing timezone utility for date/time handling

# Serializer for User model
class UserSerializer(serializers.ModelSerializer):
    # Password field will be write-only and requires a minimum length of 8 characters
    password = serializers.CharField(write_only=True, required=True, min_length=8)

    class Meta:
        model = User  # Specifying the model to serialize
        fields = ['id', 'username', 'email', 'password']  # Defining fields to be included in the serialized output

    def create(self, validated_data):
        # Creating a new user with validated data
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email'),
            password=validated_data['password']
        )
        return user  # Returning the created user

# Serializer for Task model
class TaskSerializer(serializers.ModelSerializer):
    # Read-only field for owner, displaying the username of the owner
    owner = serializers.ReadOnlyField(source='owner.username')
    # Read-only field for completed_at, to show when the task was completed
    completed_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Task  # Specifying the model to serialize
        fields = ['id', 'owner', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'created_at', 'updated_at']  # Fields to include in serialization
        read_only_fields = ['status', 'completed_at', 'created_at', 'updated_at']  # Defining read-only fields

    def validate_due_date(self, value):
        # Validating that the due date is in the future
        if value <= timezone.now():
            raise serializers.ValidationError("Due date must be in the future.")
        return value  # Returning the valid due date

    def validate_priority(self, value):
        # Validating that the priority is one of the predefined choices
        valid_priorities = [choice[0] for choice in Task.PRIORITY_LEVELS]
        if value not in valid_priorities:
            raise serializers.ValidationError(f"Priority must be one of {valid_priorities}.")
        return value  # Returning the valid priority

    def update(self, instance, validated_data):
        # Preventing updates to completed tasks unless reverted to incomplete
        if instance.status == 'Completed':
            raise serializers.ValidationError("Cannot edit a completed task unless it is marked as incomplete.")
        return super().update(instance, validated_data)  # Proceeding with the update for valid tasks
