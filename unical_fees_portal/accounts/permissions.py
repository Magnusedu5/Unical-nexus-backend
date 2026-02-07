from rest_framework.permissions import BasePermission
from .models import User

class IsAdmin(BasePermission):
    """
    Custom permission to only allow users with the ADMIN role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Roles.ADMIN)


class IsStudent(BasePermission):
    """
    Custom permission to only allow users with the STUDENT role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Roles.STUDENT)

class IsStaff(BasePermission):
    """
    Custom permission to only allow users with the STAFF role.
    """
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == User.Roles.STAFF)