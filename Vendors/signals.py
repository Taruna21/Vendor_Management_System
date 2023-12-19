from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework import status
from rest_framework.response import Response

from .models import PurchaseOrder, VendorPerformance


@receiver(pre_save, sender=PurchaseOrder)
def calculate_response_time(sender, instance, **kwargs):
    """
        Calculates response time and saves to VendorPerformance.
        Address three cases:
        1. If PO is acknowledged already, acknowledgement date should not change and
            the response time should not be computed.
        2. Allow acknowledgement only if status is pending.
        3. Allow other status to take effect e.g. shipping, completed or cancelled.
           Without updating acknowledgement date
        """
    try:
        old_instance = sender.objects.get(pk=instance.pk)
    except sender.DoesNotExist:
        return  # End execution

    if instance.status == old_instance.status:  # issue 1
        return  # Status remains unchanged, no need to process further

    elif instance.status == 'acknowledged' and old_instance.status == 'pending':  # issue 2
        instance.acknowledgment_date = timezone.now()  # set acknowledgement date to now
        response_time = instance.acknowledgment_date - instance.issue_date
        response_time = response_time.total_seconds() / (24 * 3600)  # assume decimal days for response time
        # update Vendor performance
        vendor = instance.vendor
        # other given default= 0 to implement signal logic per field, this will change
        vendor_performance = VendorPerformance(vendor=vendor, purchase_order=instance, response_time=response_time)
        vendor_performance.save()
    else:  # issue 3
        return  # allow update to ship, completed or cancelled.
        # acknowledgement date shouldn't be updated
