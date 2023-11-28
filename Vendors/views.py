from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import VendorSerializers
from .models import Vendor
from django.shortcuts import get_object_or_404

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Create' : '/create-vendor/',
        'List'   : '/list-vendor/',
        'Details': '/specific-vendor',
        'Update' : '/update-vendor/',
        'Delete' : '/delete-vendor'

    }
    return Response(api_urls)
    # POST /api/vendors/: Create a new vendor.
    # GET /api/vendors/: List all vendors.
    # GET /api/vendors/{vendor_id}/: Retrieve a specific vendor's details.
    # PUT /api/vendors/{vendor_id}/: Update a vendor's details.
    # DELETE /api/vendors/{vendor_id}/: Delete a vendor


