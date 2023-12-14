from django.db import models
from django.utils import timezone
from django.db.models import JSONField

from Accounts.models import CustomUser


def generate_vendor_code():
    """Generate a random vendor code based on a pattern"""
    last_code = Vendor.objects.all().order_by('-vendor_code').first()
    if last_code:
        last_number = int(last_code.vendor_code[1:])
        new_number = last_number + 1
        new_code = f"v{new_number:02d}"
    else:
        new_code = "v01"
    return new_code


class Vendor(models.Model):
    vendor_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile', unique=True)
    vendor_code = models.CharField(max_length=250, default=generate_vendor_code, editable=False, blank=True)

    def __str__(self):
        return self.name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('acknowledged', 'Acknowledged'),
        ('shipping', 'Shipping'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    po_number = models.CharField(max_length=100, unique=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating = models.FloatField()
    response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"{self.vendor.name} - {self.date}"


class VendorPerformanceAverages(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    average_on_time_delivery_rate = models.FloatField()
    average_quality_rating = models.FloatField()
    average_response_time = models.FloatField()
    average_fulfillment_rate = models.FloatField()
