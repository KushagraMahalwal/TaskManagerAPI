# permissions.py
from rest_framework import permissions
class IsAdminOrOwner(permissions.BasePermission):
    """
    Custom permission:
    - Admins (is_staff=True) can access all tasks.
    - Regular users can only access their own tasks.
    """

    def has_object_permission(self, request, view, obj):
        # Admin can do anything
        if request.user.is_staff:
            return True

        # Regular user can only access their own object
        return obj.user == request.user


class IsAdminToDelete(permissions.BasePermission):
    def has_permission(self, request, view):
        # Only allow DELETE if user is admin
        if request.method == "DELETE":
            return request.user.is_staff
        return True