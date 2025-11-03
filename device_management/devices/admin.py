from django.contrib import admin
from .models import Category, Brand, Location, Device, Spec


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "created_at", "updated_at"]
    search_fields = ["name", "description"]
    list_filter = ["created_at"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["name", "country", "website", "created_at"]
    search_fields = ["name", "country"]
    list_filter = ["country", "created_at"]


@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ["name", "location_type", "capacity", "created_at"]
    search_fields = ["name", "address"]
    list_filter = ["location_type", "created_at"]


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "serial_number",
        "category",
        "brand",
        "status",
        "condition",
        "location",
        "created_at",
    ]
    search_fields = ["name", "serial_number", "inventory_number"]
    list_filter = ["status", "condition", "category", "brand", "created_at"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Spec)
class SpecAdmin(admin.ModelAdmin):
    list_display = ["device", "spec_type", "value", "created_at"]
    search_fields = ["device__name", "value"]
    list_filter = ["spec_type", "created_at"]
