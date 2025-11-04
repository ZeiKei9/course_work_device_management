from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=100, unique=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Brand"
        verbose_name_plural = "Brands"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    LOCATION_TYPES = [
        ("WAREHOUSE", "Warehouse"),
        ("OFFICE", "Office"),
        ("STORAGE", "Storage"),
    ]

    name = models.CharField(max_length=100)
    location_type = models.CharField(
        max_length=20, choices=LOCATION_TYPES, default="WAREHOUSE"
    )
    address = models.TextField(blank=True, null=True)
    capacity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Location"
        verbose_name_plural = "Locations"
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.get_location_type_display()})"


class Device(models.Model):
    STATUS_CHOICES = [
        ("AVAILABLE", "Available"),
        ("RESERVED", "Reserved"),
        ("LOANED", "Loaned"),
        ("IN_SERVICE", "In Service"),
        ("RETIRED", "Retired"),
    ]

    CONDITION_CHOICES = [
        ("EXCELLENT", "Excellent"),
        ("GOOD", "Good"),
        ("FAIR", "Fair"),
        ("POOR", "Poor"),
    ]

    name = models.CharField(max_length=200)
    serial_number = models.CharField(max_length=100, unique=True)
    inventory_number = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT, related_name="devices"
    )
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="devices")
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="devices",
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="AVAILABLE"
    )
    purchase_date = models.DateField(null=True, blank=True)
    purchase_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    warranty_until = models.DateField(null=True, blank=True)
    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, default="GOOD"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Device"
        verbose_name_plural = "Devices"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} ({self.serial_number})"

    def is_available(self):
        return self.status == "AVAILABLE"

    def get_specifications(self):
        return self.specifications.all()

    def get_full_name(self):
        return f"{self.brand.name} {self.name}"


class Spec(models.Model):
    SPEC_TYPE_CHOICES = [
        ("CPU", "Processor"),
        ("RAM", "RAM"),
        ("STORAGE", "Storage"),
        ("SCREEN", "Screen Size"),
        ("COLOR", "Color"),
        ("OS", "Operating System"),
        ("OTHER", "Other"),
    ]

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="specifications"
    )
    spec_type = models.CharField(max_length=20, choices=SPEC_TYPE_CHOICES)
    value = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Specification"
        verbose_name_plural = "Specifications"
        ordering = ["spec_type"]

    def __str__(self):
        return f"{self.device.name} - {self.get_spec_type_display()}: {self.value}"


class Document(models.Model):
    DOC_TYPE_CHOICES = [
        ("MANUAL", "Manual"),
        ("WARRANTY", "Warranty"),
        ("RECEIPT", "Receipt"),
        ("CONTRACT", "Contract"),
        ("OTHER", "Other"),
    ]

    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="documents"
    )
    doc_type = models.CharField(max_length=20, choices=DOC_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="documents/%Y/%m/%d/")
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Document"
        verbose_name_plural = "Documents"
        ordering = ["-uploaded_at"]

    def __str__(self):
        return f"{self.device.name} - {self.get_doc_type_display()}: {self.title}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("CANCELLED", "Cancelled"),
        ("COMPLETED", "Completed"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    device = models.ForeignKey(
        Device, on_delete=models.CASCADE, related_name="reservations"
    )
    reserved_from = models.DateTimeField()
    reserved_until = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Reservation"
        verbose_name_plural = "Reservations"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.device.name} ({self.status})"


class Loan(models.Model):
    STATUS_CHOICES = [
        ("ACTIVE", "Active"),
        ("OVERDUE", "Overdue"),
        ("RETURNED", "Returned"),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name="loans")
    manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="managed_loans"
    )
    loaned_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="ACTIVE")
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Loan"
        verbose_name_plural = "Loans"
        ordering = ["-loaned_at"]

    def __str__(self):
        return f"{self.user.username} - {self.device.name} ({self.status})"


class Return(models.Model):
    loan = models.OneToOneField(
        Loan, on_delete=models.CASCADE, related_name="return_record"
    )
    returned_at = models.DateTimeField(auto_now_add=True)
    condition = models.CharField(max_length=20, choices=Device.CONDITION_CHOICES)
    inspected_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="inspected_returns"
    )
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Return"
        verbose_name_plural = "Returns"
        ordering = ["-returned_at"]

    def __str__(self):
        return f"Return: {self.loan.device.name} by {self.loan.user.username}"
