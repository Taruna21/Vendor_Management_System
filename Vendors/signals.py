from django.db.models import Avg
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
import datetime

from .models import PurchaseOrder, VendorPerformance, VendorPerformanceAverage, Vendor


@receiver(pre_save, sender=PurchaseOrder)
def calculate_response_time(sender, instance, **kwargs):
    """
        Calculates response time and saves to VendorPerformance Model.
        Address three cases:
        1. If PO is acknowledged already, acknowledgement date should not change and
            the response time should not be computed.
        2. Allow acknowledgement only if status is pending.
           a. update acknowledgement date
           b. update response time
        3. Allow other status to take effect e.g. shipping, completed or cancelled.
           Without updating acknowledgement date.
        4. Estimate delivery date.
        """
    initial_delivery_time = 7  # Initial assumed value
    vendor = instance.vendor
    try:
        old_instance = sender.objects.get(pk=instance.pk)  # Fetch existing status instance on db for comparison
    except sender.DoesNotExist:
        return  # End execution

    if instance.status == old_instance.status:  # issue 1
        return  # Status remains unchanged, no need to process further

    if instance.status == 'acknowledged' and old_instance.status == 'pending':  # issue 2
        # Set acknowledgment_date
        instance.acknowledgment_date = timezone.now()  # set acknowledgement date to now

        #  Calculate and update delivery date
        try:
            vendor_av_stats = get_object_or_404(VendorPerformanceAverage, vendor=vendor)  # fetch Vendor average starts
            days_to_delivery = vendor_av_stats.average_response_time  # get average response time

        except Http404:
            days_to_delivery = initial_delivery_time  # set first instance to initial_delivery_time

        instance.delivery_date = old_instance.order_date + datetime.timedelta(
            days=+max(days_to_delivery, initial_delivery_time))

        # update VendorPerformance
        # Calculate response time
        response_time = instance.acknowledgment_date - instance.issue_date  # compute response. result is a time delta
        response_time = round((response_time.total_seconds() / (24 * 3600)), 2)  # assume decimal days for response time
        vendor_performance = VendorPerformance(vendor=vendor, purchase_order=instance, response_time=response_time)
        vendor_performance.save()

    elif instance.status not in ['acknowledged', 'pending']:  # issue 3
        # Allow update to ship, completed, or cancelled without updating acknowledgment date
        return  # Acknowledgement date shouldn't be updated in these cases


@receiver(post_save, sender=PurchaseOrder)
def calculate_vendor_average_stats(sender, instance, **kwargs):
    """
    Anytime the VendorPerformance is updated. Calculate average values and save to VendorPerformanceAverage Model.
    Since we want to calculate the average for each Vendor. There should be only one record/instance of vendor in the
    VendorPerformanceAverage model.
    """
    vendor = instance.vendor  # fetch vendor
    # filter all Performance records related to a particular Vendor
    vendor_performance = VendorPerformance.objects.filter(vendor=vendor)
    # Calculate averages
    average_response_time = vendor_performance.aggregate(Avg('response_time'))['response_time__avg']
    # average_on_time_delivery_rate =
    # average_quality_rating =
    # average_fulfillment_rate =

    # create instance or get if it exists
    vendor_performance, created = VendorPerformanceAverage.objects.get_or_create(
        vendor=vendor,
        defaults={
            'average_on_time_delivery_rate': 0,
            'average_quality_rating': 0,
            'average_response_time': average_response_time,
            'average_fulfillment_rate': 0
        }
    )

    if created:
        print(f"created: {created}")
        return  # New instance created with values provided
    if not created:
        # Update old instance with new average values
        print(f"created: {created}")
        vendor_performance.average_response_time = average_response_time
        # vendor_performance.average_on_time_delivery_rate = average_on_time_delivery_rate
        # vendor_performance.average_quality_rating = average_quality_rating
        # vendor_performance.average_fulfillment_rate = average_quality_rating
        vendor_performance.save()
