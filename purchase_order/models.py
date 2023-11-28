from django.db import models
from vendors.models import Vendor
from django.utils import timezone
# Create your models here.
from django.contrib.postgres.fields import JSONField

class PurchaseOrder():
    po_number = models.CharField(max_length=100 , unique=True)
    vendor =  models.ForeignKey(Vendor, on_delete= models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now)
    delivery_date = models.DateTimeField(null=True, blank=True)
    items = JSONField()
    quantity = models.PositiveIntegerField()
    status = models.CharField(max_length=20, default='pending')
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField(auto_now_add=True)
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO #{self.po_number} - Vendor: {self.vendor.name}"