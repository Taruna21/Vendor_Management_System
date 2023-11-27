from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Vendor(models.Model):
    name = models.CharField(max_length=100)
    contact_detils = PhoneNumberField()
    address = models.CharField(max_length=100)
    vendor_code = models.CharField(max_length=50 , unique= True)
