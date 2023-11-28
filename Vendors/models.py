from django.db import models

# Create your models here.


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