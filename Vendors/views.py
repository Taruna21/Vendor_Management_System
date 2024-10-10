# Vendors/views.py
from django.http import Http404
from django.shortcuts import get_object_or_404
# import schema decorators
from drf_spectacular.utils import extend_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from Accounts.models import CustomUser

from .models import Vendor, PurchaseOrder, VendorPerformanceAverage
from .serializers import VendorSerializer, PurchaseOrderSerializer, VendorPerformanceSerializer


class VendorListCreateView(APIView):
    @extend_schema(
        description="Retrieve a list of vendors.",
        responses={200: VendorSerializer(many=True)},
    )
    def get(self, request):
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create a new vendor.",
        request=VendorSerializer,
        responses={201: {'Success': 'Vendor created successfully'}, 400: VendorSerializer()},
    )
    def post(self, request):
        try:
            user_id = int(request.data.get('vendor_user'))  # possible ValueError
            user = get_object_or_404(CustomUser, pk=user_id)  # check user exist

            # Serialize request data
            serializer = VendorSerializer(data=request.data)
            if serializer.is_valid():
                vendor = serializer.save()  # Save the vendor data
                return Response({'Success': 'Vendor created successfully'}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except ValueError:
            return Response({'Error': 'Invalid value for vendor_user.Must be int'}, status=status.HTTP_400_BAD_REQUEST)

        except Http404:
            return Response({'Error': f"User with id {user_id} doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({'Error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class VendorRetrieveUpdateDestroyView(APIView):
    @extend_schema(
        description="Retrieve a specific vendor.",
        responses={200: VendorSerializer()},
    )
    def get(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            serializer = VendorSerializer(vendor)
            return Response(serializer.data)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

    @extend_schema(
        description="Update a specific vendor.",
        request=VendorSerializer,
        responses={200: VendorSerializer(), 400: VendorSerializer()},
    )
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

    @extend_schema(description="Delete a specific vendor.", responses={204: None})
    def delete(self, request, vendor_id):
        try:
            vendor = Vendor.objects.get(pk=vendor_id)
            vendor.delete()
            return Response({'message': 'Vendor deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except Vendor.DoesNotExist:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)


class PurchaseOrderListCreateView(APIView):
    @extend_schema(
        description="Retrieve a list of purchase orders.",
        request=PurchaseOrderSerializer,
        responses={200: PurchaseOrderSerializer(many=True)},
    )
    def get(self, request):
        vendor_filter = request.query_params.get('vendor', None)
        if vendor_filter:
            purchase_orders = PurchaseOrder.objects.filter(vendor_reference=vendor_filter)
        else:
            purchase_orders = PurchaseOrder.objects.all()

        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    @extend_schema(
        description="Create a new purchase order.",
        request=PurchaseOrderSerializer,
        responses={201: PurchaseOrderSerializer(), 400: PurchaseOrderSerializer()},
    )
    def post(self, request):
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PurchaseOrderRetrieveUpdateDeleteView(APIView):
    @extend_schema(description="Retrieve a specific purchase order.", responses={200: PurchaseOrderSerializer()})
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

    @extend_schema(
        description="Update a specific purchase order.",
        request=PurchaseOrderSerializer,
        responses={200: PurchaseOrderSerializer(), 400: PurchaseOrderSerializer()},
    )
    def put(self, request, po_id):
        return self.update_purchase_order(request, po_id)

    @extend_schema(description="Partially update a specific purchase order.", request=PurchaseOrderSerializer)
    def patch(self, request, po_id):
        return self.update_purchase_order(request, po_id, partial=True)

    @extend_schema(description="Delete a specific purchase order.", responses={204: None})
    def delete(self, request, po_id):
        try:
            purchase_order = PurchaseOrder.objects.get(pk=po_id)
            purchase_order.delete()
            return Response({'message': 'Purchase Order deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
        except PurchaseOrder.DoesNotExist:
            return Response({'error': 'Purchase Order not found'}, status=status.HTTP_404_NOT_FOUND)


class VendorPerformanceListView(APIView):
    def get(self, request, vendor_id):
        try:
            vendor = get_object_or_404(Vendor, pk=vendor_id)
        except Http404:
            return Response({'error': 'Vendor not found'}, status=status.HTTP_404_NOT_FOUND)

        vendor_performances = VendorPerformanceAverage.objects.get(vendor=vendor)
        serializer = VendorPerformanceSerializer(vendor_performances)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)
