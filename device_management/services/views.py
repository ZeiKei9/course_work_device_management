from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Payment, ServiceOrder
from .permissions import IsManagerOrAdmin, IsOwnerOrReadOnly
from .serializers import PaymentSerializer, ServiceOrderSerializer


class ServiceOrderViewSet(viewsets.ModelViewSet):
    queryset = (
        ServiceOrder.objects.select_related("device", "assigned_to", "created_by")
        .prefetch_related("works")
        .all()
    )
    serializer_class = ServiceOrderSerializer
    permission_classes = [IsManagerOrAdmin]
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


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related(
        "paid_by", "related_loan", "related_service_order"
    ).all()
    serializer_class = PaymentSerializer
    permission_classes = [IsOwnerOrReadOnly]
    filter_backends = [
        filters.SearchFilter,
        filters.OrderingFilter,
        DjangoFilterBackend,
    ]
    search_fields = ["paid_by__username"]
    ordering_fields = ["paid_at", "amount"]
    ordering = ["-paid_at"]
    filterset_fields = [
        "payment_type",
        "paid_by",
        "related_loan",
        "related_service_order",
    ]

    def get_queryset(self):
        if self.request.user.is_staff:
            return self.queryset

        try:
            profile = self.request.user.profile
            if profile.role and profile.role.name in ["MANAGER", "ADMIN"]:
                return self.queryset
        except:
            pass

        return self.queryset.filter(paid_by=self.request.user)

    def perform_create(self, serializer):
        serializer.save(paid_by=self.request.user)

    @action(detail=False, methods=["get"])
    def my_payments(self, request):
        my_payments = self.queryset.filter(paid_by=request.user)
        serializer = self.get_serializer(my_payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def by_type(self, request):
        payment_type = request.query_params.get("type", None)
        if not payment_type:
            return Response(
                {"error": "Payment type is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        payments = self.get_queryset().filter(payment_type=payment_type)
        serializer = self.get_serializer(payments, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def total_by_user(self, request):
        from django.db.models import Sum

        user_id = request.query_params.get("user", None)
        if not user_id:
            user_id = request.user.id

        queryset = self.get_queryset()
        total = queryset.filter(paid_by_id=user_id).aggregate(total=Sum("amount"))
        return Response({"user_id": user_id, "total_amount": total["total"] or 0})
