from rest_framework import permissions


class PostCommentObjectPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated or request.method in permissions.SAFE_METHODS:
            return True
        return False

    def has_object_permission(self, request, view, obj):

        if request.method in permissions.SAFE_METHODS:
            return True

        if request.user.is_superuser:
            return True

        if request.method in ['POST', 'PATCH'] and request.user.is_authenticated:
            return True

        if request.user == obj.author:
            return True
        return False
