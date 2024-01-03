from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class AutoDateTimeField(models.DateTimeField):
    def pre_save(self, model_instance, add):
        return timezone.now()


class Vendor(models.Model):
    name = models.CharField(max_length=200, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class PurchaseOrderManager(models.Manager):
    def get_queryset_for_vendor(self, user):
        return self.filter(vendor__user=user, vendor__isnull=False)


class PurchaseOrder(models.Model):
    STATUS_CHOICES = (
        ("NOT_STARTED", "Not started"),
        ("IN_PROCESS", "In process"),
        ("CLOSED", "Closed"),
    )

    order_number = models.CharField(max_length=100)
    supplier_ack = models.CharField(max_length=255, blank=True, null=True)
    eta = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="NOT_STARTED"
    )
    comments = models.TextField(blank=True, null=True)

    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True)

    updated_at = AutoDateTimeField(default=timezone.now)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"PurchaseOrder #{self.order_number}"

    objects = PurchaseOrderManager()


class PurchaseOrderItem(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    part_number = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    description = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"PN: {self.part_number} ({self.quantity})"


class PurchaseOrderHistory(models.Model):
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    status = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(default=timezone.now)

    def __str__(self):
        return f"Status changed by {self.created_by} at {self.created_at}"
