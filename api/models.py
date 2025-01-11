from django.db import models
from django.contrib.auth.models import User  # Importing the User model for user authentication
from django.utils import timezone  # Importing timezone to handle time-related functionality

# Defining the Task model
class Task(models.Model):
    # Priority levels for the task
    PRIORITY_LEVELS = [
        ('Low', 'Low'),        # Option for low priority
        ('Medium', 'Medium'),  # Option for medium priority
        ('High', 'High'),      # Option for high priority
    ]

    # Status choices for the task
    STATUS_CHOICES = [
        ('Pending', 'Pending'),    # Option for pending tasks
        ('Completed', 'Completed'), # Option for completed tasks
    ]

    # Foreign key to link each task to a specific user (owner)
    owner = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    
    # Fields for the Task model
    title = models.CharField(max_length=255)  # Title of the task
    description = models.TextField(blank=True)  # Description of the task, can be blank
    due_date = models.DateTimeField()  # Due date for the task
    priority = models.CharField(max_length=10, choices=PRIORITY_LEVELS, default='Medium')  # Priority level with a default value
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')  # Current status with a default value
    completed_at = models.DateTimeField(null=True, blank=True)  # Timestamp for when the task was completed

    # Timestamps for tracking creation and last update times
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when the task is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set when the task is updated

    # Method to mark the task as completed
    def mark_completed(self):
        self.status = 'Completed'  # Change status to completed
        self.completed_at = timezone.now()  # Set the completed timestamp to the current time
        self.save()  # Save the changes to the database

    # Method to mark the task as incomplete
    def mark_incomplete(self):
        self.status = 'Pending'  # Change status back to pending
        self.completed_at = None  # Clear the completed timestamp
        self.save()  # Save the changes to the database

    # String representation of the task, returns the title
    def __str__(self):
        return self.title

