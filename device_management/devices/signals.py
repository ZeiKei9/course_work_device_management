from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from .models import Loan, Return, Device


@receiver(post_save, sender=Loan)
def update_device_status_on_loan(sender, instance, created, **kwargs):
    if created:
        device = instance.device
        device.status = "LOANED"
        device.save()


@receiver(post_save, sender=Return)
def update_device_status_on_return(sender, instance, created, **kwargs):
    if created:
        loan = instance.loan
        loan.status = "RETURNED"
        loan.save()

        device = loan.device
        device.status = "AVAILABLE"
        device.condition = instance.condition
        device.save()


@receiver(pre_save, sender=Loan)
def check_overdue_loan(sender, instance, **kwargs):
    if instance.pk:
        if instance.status == "ACTIVE" and instance.due_date < timezone.now():
            instance.status = "OVERDUE"
