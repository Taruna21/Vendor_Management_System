from django.db.models import Avg
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response

from .models import PurchaseOrder, VendorPerformance, VendorPerformanceAverage, Vendor


@receiver(pre_save, sender=PurchaseOrder)
def calculate_response_time(sender, instance, **kwargs):
    """
        Calculates response time and saves to VendorPerformance Model.
        Address three cases:
        1. If PO is acknowledged already, acknowledgement date should not change and
            the response time should not be computed.
        2. Allow acknowledgement only if status is pending.
        3. Allow other status to take effect e.g. shipping, completed or cancelled.
           Without updating acknowledgement date.
        """
    try:
        old_instance = sender.objects.get(pk=instance.pk)  # Fetch existing status instance on db for comparison
    except sender.DoesNotExist:
        return  # End execution

    if instance.status == old_instance.status:  # issue 1
        return  # Status remains unchanged, no need to process further

    elif instance.status == 'acknowledged' and old_instance.status == 'pending':  # issue 2
        instance.acknowledgment_date = timezone.now()  # set acknowledgement date to now
        response_time = instance.acknowledgment_date - instance.issue_date  # compute response. result is a time delta
        response_time = round((response_time.total_seconds() / (24 * 3600)), 2)  # assume decimal days for response time
        # update Vendor performance
        vendor = instance.vendor
        # other fields set to default= 0 to implement signal logic per field, this will change
        vendor_performance = VendorPerformance(vendor=vendor, purchase_order=instance, response_time=response_time)
        vendor_performance.save()
    else:  # issue 3
        return  # allow update to ship, completed or cancelled.
        # acknowledgement date shouldn't be updated in this cases


@receiver(post_save, sender=PurchaseOrder)
def calculate_vendor_average_stats(sender, instance, **kwargs):
    """
    Anytime the VendorPerformance is updated. Calculate average values and save to VendorPerformanceAverage Model.
    Since we want to calculate the average for each Vendor. There should be only one record/instance of vendor on the
    VendorPerformanceAverage model.

    """
    vendor = instance.vendor  # fetch vendor
    # filter all Performance records related to a particular Vendor
    vendor_performance = VendorPerformance.objects.filter(vendor=vendor)
    # Calculate averages
    vendor_average_response_time = vendor_performance.aggregate(Avg('response_time'))['response_time__avg']
    # create instance or get if it exists
    obj_performance, created = VendorPerformanceAverage.objects.get_or_create(
        vendor=vendor,
        defaults={
            'average_response_time': vendor_average_response_time,
            'average_on_time_delivery_rate': 0,
            'average_quality_rating': 0,
            'average_response_time': 0,
            'average_fulfillment_rate': 0
        }
    )

    if created:
        return  # New instance created with values provided
    if not created:
        # Update old instance with new average values
        obj_performance.average_response_time = vendor_average_response_time
        obj_performance.save()

