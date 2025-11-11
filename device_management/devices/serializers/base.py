from rest_framework import serializers
from devices.models import Category, Brand, Location, Spec, Document


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
