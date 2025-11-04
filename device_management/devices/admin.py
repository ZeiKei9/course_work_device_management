from django.contrib import admin
from .models import Category, Brand, Location, Device, Spec, Document, Reservation, Loan


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
    fieldsets = [
        (
            "Basic Information",
            {
                "fields": [
                    "name",
                    "serial_number",
                    "inventory_number",
                    "category",
                    "brand",
                ]
            },
        ),
        ("Status", {"fields": ["status", "condition", "location"]}),
        (
            "Purchase Information",
            {"fields": ["purchase_date", "purchase_price", "warranty_until"]},
        ),
        ("Additional", {"fields": ["notes", "created_at", "updated_at"]}),
    ]


@admin.register(Spec)
class SpecAdmin(admin.ModelAdmin):
    list_display = ["device", "spec_type", "value", "created_at"]
    search_fields = ["device__name", "value"]
    list_filter = ["spec_type", "created_at"]


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ["device", "doc_type", "title", "uploaded_at"]
    search_fields = ["device__name", "title"]
    list_filter = ["doc_type", "uploaded_at"]


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = [
        "user",
        "device",
        "reserved_from",
        "reserved_until",
        "status",
        "created_at",
    ]
    search_fields = ["user__username", "device__name"]
    list_filter = ["status", "created_at"]
    readonly_fields = ["created_at", "updated_at"]


@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ["user", "device", "manager", "loaned_at", "due_date", "status"]
    search_fields = ["user__username", "device__name", "manager__username"]
    list_filter = ["status", "loaned_at"]
    readonly_fields = ["loaned_at", "created_at", "updated_at"]
