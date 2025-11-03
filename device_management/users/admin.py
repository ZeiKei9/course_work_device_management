from django.contrib import admin
from .models import Role


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    list_filter = ['name', 'created_at']