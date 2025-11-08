from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    """
    Allows access only to users with the 'User' role.
    """
    def has_permission(self, request, view):
        return request.user and request.user.role == 'User'
