from rest_framework import permissions


class IsUserInAPIGroup(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        api_group_users = ...
        if request.user in api_group_users:
            return True
