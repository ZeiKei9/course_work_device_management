from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import ServiceOrder
from .serializers import ServiceOrderSerializer


class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = (
        ServiceOrder.objects.select_related("device", "assigned_to", "created_by")
        .prefetch_related("works")
        .all()
    )
    serializer_class = ServiceOrderSerializer
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["device__name", "device__serial_number", "issue_description"]
    ordering_fields = ["created_at", "priority"]
    ordering = ["-created_at"]
    filterset_fields = ["status", "priority", "assigned_to", "device"]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

    @action(detail=False, methods=["get"])
    def pending(self, request):
        pending_orders = self.queryset.filter(status="PENDING")
        serializer = self.get_serializer(pending_orders, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def in_progress(self, request):
        in_progress_orders = self.queryset.filter(status="IN_PROGRESS")
        serializer = self.get_serializer(in_progress_orders, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def complete(self, request, pk=None):
        from django.utils import timezone

        service_order = self.get_object()
        if service_order.status in ["PENDING", "IN_PROGRESS"]:
            service_order.status = "COMPLETED"
            service_order.completed_at = timezone.now()
            service_order.save()
            return Response({"status": "Service order completed"})
        return Response(
            {"error": "Can only complete pending or in-progress orders"},
            status=status.HTTP_400_BAD_REQUEST,
        )
