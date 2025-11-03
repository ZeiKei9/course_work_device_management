from django.db import models
from django.contrib.auth.models import User


class Role(models.Model):
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('MANAGER', 'Manager'),
        ('USER', 'User'),
    ]

    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    permissions = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
        ordering = ['name']

    def __str__(self):
        return self.get_name_display()