from rest_framework import serializers
from .models import Category, Brand, Location, Device, Spec, Document, Reservation, Loan


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "description", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "country", "website", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]


class LocationSerializer(serializers.ModelSerializer):
    location_type_display = serializers.CharField(
        source="get_location_type_display", read_only=True
    )

    class Meta:
        model = Location
        fields = [
            "id",
            "name",
            "location_type",
            "location_type_display",
            "address",
            "capacity",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]


class SpecSerializer(serializers.ModelSerializer):
    spec_type_display = serializers.CharField(
        source="get_spec_type_display", read_only=True
    )

    class Meta:
        model = Spec
        fields = ["id", "spec_type", "spec_type_display", "value", "created_at"]
        read_only_fields = ["created_at"]


class DocumentSerializer(serializers.ModelSerializer):
    doc_type_display = serializers.CharField(
        source="get_doc_type_display", read_only=True
    )

    class Meta:
        model = Document
        fields = [
            "id",
            "doc_type",
            "doc_type_display",
            "title",
            "file",
            "description",
            "uploaded_at",
        ]
        read_only_fields = ["uploaded_at"]


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


class ReservationSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    device_name = serializers.CharField(source="device.name", read_only=True)
    device_serial = serializers.CharField(source="device.serial_number", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "user_username",
            "device",
            "device_name",
            "device_serial",
            "reserved_from",
            "reserved_until",
            "status",
            "status_display",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate(self, attrs):
        if attrs["reserved_from"] >= attrs["reserved_until"]:
            raise serializers.ValidationError(
                "Reserved until must be after reserved from"
            )
        return attrs


class LoanSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source="user.username", read_only=True)
    manager_username = serializers.CharField(source="manager.username", read_only=True)
    device_name = serializers.CharField(source="device.name", read_only=True)
    device_serial = serializers.CharField(source="device.serial_number", read_only=True)
    status_display = serializers.CharField(source="get_status_display", read_only=True)

    class Meta:
        model = Loan
        fields = [
            "id",
            "user",
            "user_username",
            "device",
            "device_name",
            "device_serial",
            "manager",
            "manager_username",
            "loaned_at",
            "due_date",
            "status",
            "status_display",
            "notes",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["loaned_at", "created_at", "updated_at"]

    def validate(self, attrs):
        device = attrs.get("device")
        if device and not device.is_available():
            raise serializers.ValidationError("Device is not available for loan")
        return attrs
