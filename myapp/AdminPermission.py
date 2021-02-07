from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    """
    Allows access only to Admin.
    """

    def has_permission(self, request, view):
        if request.user.username == 'admin':
            return True
        else:
            return False