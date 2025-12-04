from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Brand, Category, Device, Loan, Location, Reservation, Return
from .permissions import IsAdminOrReadOnly, IsManagerOrAdmin, IsOwnerOrManager
from .serializers import (
    BrandSerializer,
    CategorySerializer,
    DeviceListSerializer,
    DeviceSerializer,
    LoanSerializer,
    LocationSerializer,
    ReservationSerializer,
    ReturnSerializer,
)
from .utils import (
    export_devices_to_csv,
    export_devices_to_excel,
    export_devices_to_json,
    export_loans_to_csv,
    export_loans_to_excel,
    export_loans_to_json,
    export_devices_to_pdf,
    export_loans_to_pdf,
)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]


class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]
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
    permission_classes = [IsAdminOrReadOnly]
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
    serializer_class = DeviceSerializer
    permission_classes = [IsManagerOrAdmin]
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

    def get_permissions(self):
        if self.action in ["list", "retrieve", "available", "by_serial"]:
            return [IsAdminOrReadOnly()]
        return [IsManagerOrAdmin()]

    @action(detail=False, methods=["get"])
    def available(self, request):
        available_devices = self.queryset.filter(status="AVAILABLE")
        serializer = DeviceListSerializer(available_devices, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_serial(self, request):
        serial = request.query_params.get("serial", None)
        if not serial:
            return Response(
                {"error": "Serial number is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            device = Device.objects.get(serial_number=serial)
            serializer = DeviceSerializer(device)
            return Response(serializer.data)
        except Device.DoesNotExist:
            return Response(
                {"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND
            )

    @action(detail=True, methods=["get"])
    def history(self, request, pk=None):
        device = self.get_object()
        loans = device.loans.all().order_by("-loaned_at")
        reservations = device.reservations.all().order_by("-created_at")
        service_orders = device.service_orders.all().order_by("-created_at")

        return Response(
            {
                "device": DeviceSerializer(device).data,
                "loans_count": loans.count(),
                "reservations_count": reservations.count(),
                "service_orders_count": service_orders.count(),
            }
        )

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_devices_to_csv(queryset)

    @action(detail=False, methods=["get"])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_devices_to_excel(queryset)

    @action(detail=False, methods=["get"])
    def export_json(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_devices_to_json(queryset)

    @action(detail=False, methods=["get"])
    def export_pdf(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_devices_to_pdf(queryset)

    @action(detail=False, methods=["get"])
    def export(self, request):
        format_type = request.query_params.get("format", "csv").lower()
        queryset = self.filter_queryset(self.get_queryset())

        if format_type == "csv":
            return export_devices_to_csv(queryset)
        elif format_type == "xlsx":
            return export_devices_to_excel(queryset)
        elif format_type == "json":
            return export_devices_to_json(queryset)
        else:
            return Response(
                {"error": "Invalid format. Use csv, xlsx, or json"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.select_related("user", "device").all()
    serializer_class = ReservationSerializer
    permission_classes = [IsOwnerOrManager]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["user__username", "device__name", "device__serial_number"]
    ordering_fields = ["created_at", "reserved_from", "reserved_until"]
    ordering = ["-created_at"]
    filterset_fields = ["status", "user", "device"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset
        try:
            profile = self.request.user.profile
            if profile.role and profile.role.name in ["MANAGER", "ADMIN"]:
                return self.queryset
        except:
            pass
        return self.queryset.filter(user=self.request.user)

    @action(detail=False, methods=["get"])
    def my_reservations(self, request):
        reservations = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(reservations, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.status == "ACTIVE":
            reservation.status = "CANCELLED"
            reservation.save()
            return Response({"status": "Reservation cancelled"})
        return Response(
            {"error": "Can only cancel active reservations"},
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.select_related("user", "device", "manager").all()
    serializer_class = LoanSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["user__username", "device__name", "device__serial_number"]
    ordering_fields = ["loaned_at", "due_date"]
    ordering = ["-loaned_at"]
    filterset_fields = ["status", "user", "device"]

    def get_permissions(self):
        if self.action in ["my_loans"]:
            from rest_framework.permissions import IsAuthenticated

            return [IsAuthenticated()]
        return [IsManagerOrAdmin()]

    def get_queryset(self):
        if self.action == "my_loans":
            return self.queryset.filter(user=self.request.user)

        if self.request.user.is_staff:
            return self.queryset

        try:
            profile = self.request.user.profile
            if profile.role and profile.role.name in ["MANAGER", "ADMIN"]:
                return self.queryset
        except:
            pass

        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(manager=self.request.user)

    @action(detail=False, methods=["get"])
    def active(self, request):
        active_loans = self.get_queryset().filter(status="ACTIVE")
        serializer = self.get_serializer(active_loans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def overdue(self, request):
        overdue_loans = self.get_queryset().filter(status="OVERDUE")
        serializer = self.get_serializer(overdue_loans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def my_loans(self, request):
        my_loans = self.queryset.filter(user=request.user)
        serializer = self.get_serializer(my_loans, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def export_csv(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_loans_to_csv(queryset)

    @action(detail=False, methods=["get"])
    def export_excel(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_loans_to_excel(queryset)

    @action(detail=False, methods=["get"])
    def export_json(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_loans_to_json(queryset)

    @action(detail=False, methods=["get"])
    def export_pdf(self, request):
        queryset = self.filter_queryset(self.get_queryset())
        return export_loans_to_pdf(queryset)

    @action(detail=False, methods=["get"])
    def export(self, request):
        format_type = request.query_params.get("format", "csv").lower()
        queryset = self.filter_queryset(self.get_queryset())

        if format_type == "csv":
            return export_loans_to_csv(queryset)
        elif format_type == "xlsx":
            return export_loans_to_excel(queryset)
        elif format_type == "json":
            return export_loans_to_json(queryset)
        else:
            return Response(
                {"error": "Invalid format. Use csv, xlsx, or json"},
                status=status.HTTP_400_BAD_REQUEST,
            )


class ReturnViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.select_related(
        "loan", "loan__device", "loan__user", "inspected_by"
    ).all()
    serializer_class = ReturnSerializer
    permission_classes = [IsManagerOrAdmin]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["loan__user__username", "loan__device__name"]
    ordering_fields = ["returned_at"]
    ordering = ["-returned_at"]
    filterset_fields = ["condition", "inspected_by"]

    def perform_create(self, serializer):
        serializer.save(inspected_by=self.request.user)
