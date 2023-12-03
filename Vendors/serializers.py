from rest_framework import serializers
from .models import Vendor , PurchaseOrder , HistoricalPerformance

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendor
        fields = ['name', 'contact_details', 'address', 'vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model= PurchaseOrder
        fields = ['po_number ', 'vendor', ' order_date', 
                  'delivery_date', 'items', 'quantity','status']

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'


        

