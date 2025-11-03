from django.contrib import admin
from .models import Role, UserProfile


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["name", "created_at"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "phone", "department", "created_at"]
    search_fields = ["user__username", "phone", "department"]
    list_filter = ["role", "created_at"]
