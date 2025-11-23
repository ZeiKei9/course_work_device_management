from rest_framework import permissions


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


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        if hasattr(obj, "paid_by"):
            return obj.paid_by == request.user

        if hasattr(obj, "created_by"):
            return obj.created_by == request.user

        return False
