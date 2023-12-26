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


def generate_po_code():
    """Generate a random po code based on a pattern"""
    last_code = PurchaseOrder.objects.all().order_by('-po_number').first()
    if last_code:
        last_number = int(last_code.po_number[2:])
        new_number = last_number + 1
        new_code = f"po{new_number:02d}"
    else:
        new_code = "po01"
    return new_code


class Vendor(models.Model):
    vendor_user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile', unique=True)
    vendor_code = models.CharField(max_length=250, default=generate_vendor_code, editable=False, blank=True)

    def __str__(self):
        return self.vendor_user.first_name


class PurchaseOrder(models.Model):
    STATUS_CHOICES = [
        # ('pending', 'Pending'), # set as default value, deactivate or delete
        ('acknowledged', 'Acknowledged'),
        ('shipping', 'Shipping'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]
    po_number = models.CharField(max_length=100, default=generate_po_code, editable=False, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.po_number


class VendorPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    purchase_order = models.ForeignKey(PurchaseOrder, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    on_time_delivery_rate = models.FloatField(default=0)
    quality_rating = models.FloatField(default=0)
    response_time = models.FloatField()   # no. days for a Vendor to acknowledge an order. (acknowledgement_date -
    # issue_date)
    fulfillment_rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.vendor.vendor_user.first_name} - {self.response_time}"


class VendorPerformanceAverage(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    average_on_time_delivery_rate = models.FloatField()
    average_quality_rating = models.FloatField()
    average_response_time = models.FloatField()
    average_fulfillment_rate = models.FloatField()
