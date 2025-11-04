from django.contrib import admin
from .models import ServiceOrder


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ["id", "device", "status", "priority", "assigned_to", "created_at"]
    search_fields = ["device__name", "issue_description"]
    list_filter = ["status", "priority", "created_at"]
    readonly_fields = ["created_at", "updated_at", "completed_at"]
