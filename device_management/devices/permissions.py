from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class IsManagerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        if request.user.is_staff:
            return True

        try:
            profile = request.user.profile
            return profile.role and profile.role.name in ["MANAGER", "ADMIN"]
        except:
            return False


class IsOwnerOrManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff:
            return True

        try:
            profile = request.user.profile
            if profile.role and profile.role.name in ["MANAGER", "ADMIN"]:
                return True
        except:
            pass

        if hasattr(obj, "user"):
            return obj.user == request.user

        return False
