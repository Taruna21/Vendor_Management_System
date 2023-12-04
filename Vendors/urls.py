# your_app/urls.py

from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDestroyView, PurchaseOrderListCreateView, \
    PurchaseOrderRetrieveUpdateDeleteView

urlpatterns = [
    path('Vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('Vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyView.as_view(),
         name='vendor-retrieve-update-destroy'),
    path('purchase_orders/', PurchaseOrderListCreateView.as_view(), name='purchase-order-list-create'),
    path('purchase_orders/<int:po_id>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(),
         name='purchase-order-retrieve-update-delete')
]
