from django.db import models
from django.contrib.auth.models import User
from devices.models import Device


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
