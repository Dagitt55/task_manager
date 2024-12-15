from rest_framework import permissions  # Importing Django REST Framework's permissions module

# Custom permission class to restrict access to object owners
class IsOwner(permissions.BasePermission):
    
    # Method to check if the request user has permission to access the object
    def has_object_permission(self, request, view, obj):
        # Grant permission only if the object's owner is the same as the request user
        return obj.owner == request.user