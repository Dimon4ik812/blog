from rest_framework import permissions


class IsAuthorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Разрешить чтение всем
        if request.method in permissions.SAFE_METHODS:
            return True
        # Разрешить изменение/удаление автору или админу
        return obj.author == request.user or request.user.is_staff


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_staff
