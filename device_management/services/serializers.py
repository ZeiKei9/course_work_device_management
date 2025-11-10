from rest_framework import serializers
from .models import ServiceOrder, ServiceWork, Payment


class ServiceWorkSerializer(serializers.ModelSerializer):
    performed_by_username = serializers.CharField(
        source="performed_by.username", read_only=True
    )

    class Meta:
        model = ServiceWork
        fields = [
            "id",
            "service_order",
            "work_description",
            "parts_used",
            "cost",
            "performed_by",
            "performed_by_username",
            "performed_at",
            "notes",
        ]
        read_only_fields = ["performed_at"]


class ServiceOrderSerializer(serializers.ModelSerializer):
    device_name = serializers.CharField(source="device.name", read_only=True)
    device_serial = serializers.CharField(source="device.serial_number", read_only=True)
    assigned_to_username = serializers.CharField(
        source="assigned_to.username", read_only=True
    )
    created_by_username = serializers.CharField(
        source="created_by.username", read_only=True
    )
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True
    )
    works = ServiceWorkSerializer(many=True, read_only=True)

    class Meta:
        model = ServiceOrder
        fields = [
            "id",
            "device",
            "device_name",
            "device_serial",
            "issue_description",
            "status",
            "status_display",
            "priority",
            "priority_display",
            "assigned_to",
            "assigned_to_username",
            "created_by",
            "created_by_username",
            "works",
            "created_at",
            "updated_at",
            "completed_at",
        ]
        read_only_fields = ["created_at", "updated_at", "completed_at"]


class PaymentSerializer(serializers.ModelSerializer):
    paid_by_username = serializers.CharField(source="paid_by.username", read_only=True)
    payment_type_display = serializers.CharField(
        source="get_payment_type_display", read_only=True
    )
    related_loan_info = serializers.CharField(
        source="related_loan.__str__", read_only=True
    )
    related_service_info = serializers.CharField(
        source="related_service_order.__str__", read_only=True
    )

    class Meta:
        model = Payment
        fields = [
            "id",
            "amount",
            "payment_type",
            "payment_type_display",
            "paid_by",
            "paid_by_username",
            "related_loan",
            "related_loan_info",
            "related_service_order",
            "related_service_info",
            "paid_at",
            "notes",
        ]
        read_only_fields = ["paid_at"]

    def validate(self, attrs):
        if not attrs.get("related_loan") and not attrs.get("related_service_order"):
            raise serializers.ValidationError(
                "Payment must be related to either a loan or service order"
            )
        return attrs
