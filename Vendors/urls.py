# your_app/urls.py

from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDestroyView

urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyView.as_view(), name='vendor-retrieve-update-destroy'),
]
