from rest_framework import permissions

from employees.models import Employee


class IsUserInAPIGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            user = Employee.objects.get(name=request.user)
            return user.api_user

    def has_object_permission(self, request, view, obj):
        return obj.api_user
