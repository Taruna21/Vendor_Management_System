from rest_framework import serializers

from Accounts.models import CustomUser
from Accounts.serializers import CustomUserSerializer
from .models import Vendor, PurchaseOrder, VendorPerformance


class VendorSerializer(serializers.ModelSerializer):
    # serialize and return vendor_user(instance of CustomUser)
    user_details = CustomUserSerializer(source='vendor_user', read_only=True)

    class Meta:
        model = Vendor
        fields = ['id', 'vendor_user', 'vendor_code', "user_details"]
        extra_kwargs = {
            'vendor_user': {'write_only': True}  # Marking vendor_user as write-only.
            # Will be provided from nested CustomUser
        }


class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = ['po_number', 'vendor', 'order_date',
                  'delivery_date', 'items', 'quantity', 'status']


class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = VendorPerformance
        fields = '__all__'
