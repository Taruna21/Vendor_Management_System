from Accounts.models import CustomUser
from rest_framework import serializers
from .models import Vendor, PurchaseOrder, VendorPerformance


class VendorSerializer(serializers.ModelSerializer):
    # vendor_user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Vendor
        fields = ['vendor_user_id', 'vendor_code']

    # def create(self, validated_data):


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date',
                  'delivery_date', 'items', 'quantity', 'status']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = '__all__'
