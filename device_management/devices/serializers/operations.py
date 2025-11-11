from rest_framework import serializers
from devices.models import Device
from .base import SpecSerializer, DocumentSerializer


class DeviceSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    location_name = serializers.CharField(source="location.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    condition_display = serializers.CharField(
        source="get_condition_display", read_only=True
    )
    specifications = SpecSerializer(many=True, read_only=True)
    documents = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "serial_number",
            "inventory_number",
            "category",
            "category_name",
            "brand",
            "brand_name",
            "location",
            "location_name",
            "status",
            "status_display",
            "condition",
            "condition_display",
            "purchase_date",
            "purchase_price",
            "warranty_until",
            "notes",
            "specifications",
            "documents",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class DeviceListSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Device
        fields = [
            "id",
            "name",
            "serial_number",
            "inventory_number",
            "category_name",
            "brand_name",
            "status",
            "status_display",
            "condition",
            "created_at",
        ]
