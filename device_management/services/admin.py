from django.contrib import admin
from .models import ServiceOrder, ServiceWork


@admin.register(ServiceOrder)
class ServiceOrderAdmin(admin.ModelAdmin):
    list_display = ["id", "device", "status", "priority", "assigned_to", "created_at"]
    search_fields = ["device__name", "issue_description"]
    list_filter = ["status", "priority", "created_at"]
    readonly_fields = ["created_at", "updated_at", "completed_at"]


@admin.register(ServiceWork)
class ServiceWorkAdmin(admin.ModelAdmin):
    list_display = [
        "service_order",
        "work_description",
        "cost",
        "performed_by",
        "performed_at",
    ]
    search_fields = ["service_order__device__name", "work_description"]
    list_filter = ["performed_at"]
    readonly_fields = ["performed_at"]
