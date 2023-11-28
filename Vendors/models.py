from django.db import models
from django.utils import timezone
from django.contrib.postgres.fields import JSONField



class Vendor(models.Model):
    name = models.CharField(max_length=250)
    contact_details = models.TextField(max_length=250)
    address = models.TextField(max_length=250)
    vendor_code = models.CharField(max_length=250)
    on_time_delivery_rate = models.FloatField(null=True, blank=True)
    quality_rating_avg = models.FloatField(null=True, blank=True)
    average_response_time = models.FloatField(null=True, blank=True)
    fulfillment_rate = models.FloatField(null=True, blank=True)

    
    def __str__(self):
        return self.name
    
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

    

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    
