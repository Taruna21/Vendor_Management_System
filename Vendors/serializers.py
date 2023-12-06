from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance


class VendorSerializer(serializers.ModelSerializer):
    vendor_user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())

    class Meta:
        model = Vendor
        fields = ['vendor_user', 'name', 'contact_details', 'address', 'vendor_code']


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number ', 'vendor', ' order_date',
                  'delivery_date', 'items', 'quantity', 'status']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'
