from django.db import models
from django.contrib.auth.models import User
from devices.models import Device, Loan


class ServiceOrder(models.Model):
    STATUS_CHOICES = [
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed"),
        ("CANCELLED", "Cancelled"),
    ]

    PRIORITY_CHOICES = [
        ("LOW", "Low"),
        ("MEDIUM", "Medium"),
        ("HIGH", "High"),
        ("URGENT", "Urgent"),
    ]

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="service_orders"
    )
    issue_description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="PENDING")
    priority = models.CharField(
        max_length=20, choices=PRIORITY_CHOICES, default="MEDIUM"
    )
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assigned_service_orders",
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_service_orders",
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Service Order"
        verbose_name_plural = "Service Orders"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Service #{self.id} - {self.device.name} ({self.status})"


class ServiceWork(models.Model):
    service_order = models.ForeignKey(
        ServiceOrder, on_delete=models.CASCADE, related_name="works"
    )
    work_description = models.TextField()
    parts_used = models.TextField(blank=True, null=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    performed_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="performed_works"
    )
    performed_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Service Work"
        verbose_name_plural = "Service Works"
        ordering = ["-performed_at"]

    def __str__(self):
        return (
            f"Work on {self.service_order.device.name} - {self.work_description[:50]}"
        )


class Payment(models.Model):
    PAYMENT_TYPE_CHOICES = [
        ("DEPOSIT", "Deposit"),
        ("FINE", "Fine"),
        ("SERVICE_FEE", "Service Fee"),
        ("RENTAL", "Rental Fee"),
    ]

    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPE_CHOICES)
    paid_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    related_loan = models.ForeignKey(
        Loan, on_delete=models.SET_NULL, null=True, blank=True, related_name="payments"
    )
    related_service_order = models.ForeignKey(
        ServiceOrder,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="payments",
    )
    paid_at = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
        ordering = ["-paid_at"]

    def __str__(self):
        return f"{self.get_payment_type_display()} - {self.amount} by {self.paid_by.username}"
