# Vendors/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Vendor, PurchaseOrder
from .serializers import VendorSerializer, PurchaseOrderSerializer

from django.contrib.auth.models import Group, User
from django.shortcuts import get_object_or_404
from django.http import Http404


class VendorListCreateView(APIView):
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    def post(self, request):
        # Extract the User instance associated with the Vendor. Inform if non-existent
        pk = request.data['vendor_user_id']
        try:
            user = get_object_or_404(User, pk=pk)  # fetch user
        except Http404:
            return Response({'Error': f"User with id {pk} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = VendorSerializer(data=request.data)
        if serializer.is_valid():
            try:
                vendor = serializer.save()  # Save the vendor data
            except Exception as e:
                return Response({'Error': str(e) + '.This user is already a Vendor'},
                                status=status.HTTP_400_BAD_REQUEST)

            vendor_group, created = Group.objects.get_or_create(name='Vendor')
            # Add the user to the Vendor group
            vendor_group.user_set.add(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VendorRetrieveUpdateDestroyView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializer(vendor, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            vendor.delete()
            return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)


# purchaseorder

class PurchaseOrderListCreateView(APIView):
    def get(self, request):
        vendor_filter = request.query_params.get('vendor', None)
        if vendor_filter:
            purchase_orders = PurchaseOrder.objects.filter(vendor_reference=vendor_filter)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderRetrieveUpdateDeleteView(APIView):
    def get(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            serializer = PurchaseOrderSerializer(purchase_order)
            return Response(serializer.data)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def update_purchase_order(self, request, po_id, partial=False):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            serializer = PurchaseOrderSerializer(
                purchase_order, data=request.data, partial=partial
            )
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, po_id):
        return self.update_purchase_order(request, po_id)

    def patch(self, request, po_id):
        return self.update_purchase_order(request, po_id, partial=True)

    def delete(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.delete()
            return Response({'message': 'Purchase Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)
