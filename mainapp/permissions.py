from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework import permissions


class IsOwnerOrReadOnly(BasePermission):
    """
    Настройки для проверки прав доступа к объекту.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the habit.
        return obj.user == request.user
