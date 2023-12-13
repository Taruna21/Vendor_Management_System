# Vendors/signals.py
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from Vendors.models import PurchaseOrder, VendorPerformance
from django.utils import timezone


@receiver(post_save, sender=PurchaseOrder)
def update_historical_performance(sender, instance, created, **kwargs):
    if not created:  # Check if it's an update (not a new instance)
        # calculate performance metrics
        if instance.acknowledgment_date and instance.issue_date:
            time_difference = instance.acknowledgment_date - instance.issue_date

        print(f"time_difference: {time_difference.days}")

        # Update or create HistoricalPerformance for the vendor
        # HistoricalPerformance.objects.update_or_create(
        #     vendor=instance.vendor,
        #     date=timezone.now(),  # Assuming you want to record the date of the update
        #     defaults={
        #         'on_time_delivery_rate': on_time_delivery_rate,
        #         'quality_rating_avg': quality_rating_avg,
        #         'average_response_time': average_response_time,
        #         'fulfillment_rate': fulfillment_rate,
        #     }
        # )


@receiver(pre_save, sender=PurchaseOrder)
def update_acknowledgment_date(sender, instance, **kwargs):
    original_instance = get_object_or_404(PurchaseOrder, id=instance.pk)
    if original_instance.status != instance.status and instance.status == 'acknowledged':
        instance.acknowledgment_date = timezone.now()
