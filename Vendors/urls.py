# your_app/urls.py

from django.urls import path
from .views import VendorListCreateView, VendorRetrieveUpdateDestroyView , PurchaseOrderListCreateView, PurchaseOrderRetrieveUpdateDeleteView

urlpatterns = [
    path('api/vendors/', VendorListCreateView.as_view(), name='vendor-list-create'),
    path('api/vendors/<int:vendor_id>/', VendorRetrieveUpdateDestroyView.as_view(), 
         name='vendor-retrieve-update-destroy'),
    path('api/purchase_orders/', PurchaseOrderListCreateView.as_view(), name= 'purchase-orde-list-create'),
    path('api/purchase_orers/<int:po_id>/', PurchaseOrderRetrieveUpdateDeleteView.as_view(),
          name= 'purchase-order-retrieve-update-delete')
]
