from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .models import Brand, Category, Device, Location
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    DeviceListSerializer,
    DeviceSerializer,
    LocationSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "country"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    filterset_fields = ["country"]


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "address"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]
    filterset_fields = ["location_type"]


class DeviceViewSet(viewsets.ModelViewSet):
    queryset = Device.objects.select_related(
        "category", "brand", "location"
    ).prefetch_related("specifications", "documents")
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["name", "serial_number", "inventory_number"]
    ordering_fields = ["name", "created_at", "purchase_date"]
    ordering = ["-created_at"]
    filterset_fields = ["category", "brand", "status", "condition", "location"]

    def get_serializer_class(self):
        if self.action == "list":
            return DeviceListSerializer
        return DeviceSerializer
