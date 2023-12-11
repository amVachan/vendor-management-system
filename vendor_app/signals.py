from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import PurchaseOrder, Vendor


@receiver(post_save, sender=PurchaseOrder)
def calculate_metrics(sender, instance, **kwargs):
    vendor = instance.vendor
    if 'status' in instance.get_dirty_fields():
        new_fulfilment_rate = calculate_fulfilment_rate(instance)
        vendor.fulfillment_rate = new_fulfilment_rate
        if instance.status.lower() == "completed":
            new_delivery_rate = calculate_delivery_rate(instance)
            vendor.on_time_delivery_rate = new_delivery_rate
            if instance.quality_rating:
                new_quality_rating_avg = calculate_quality_rating_avg(instance)
                vendor.quality_rating_avg = new_quality_rating_avg

    if 'acknowledgment_date' in instance.get_dirty_fields():
        if instance.acknowledgment_date:
            new_avg_response_time = calculate_avg_response_time(instance)
            vendor.average_response_time = new_avg_response_time

    vendor.save()


def calculate_delivery_rate(instance):
    return 0.0


def calculate_fulfilment_rate(instance):
    vendor = instance.vendor
    fulfilled_pos = PurchaseOrder.objects.filter(
        status='completed', vendor=vendor).count()
    total_pos = PurchaseOrder.objects.filter(
        vendor=vendor).count()
    return fulfilled_pos/total_pos


def calculate_quality_rating_avg(instance):
    vendor = instance.vendor
    quality_ratings_count = PurchaseOrder.objects.filter(
        quality_rating__isnull=False, vendor=vendor).count()
    current_rating = vendor.quality_rating_avg
    new_rating = ((current_rating*(quality_ratings_count-1)) +
                  instance.quality_rating)/quality_ratings_count
    return new_rating


def calculate_avg_response_time(instance):
    vendor = instance.vendor
    acknowledged_count = PurchaseOrder.objects.filter(
        acknowledgment_date__isnull=False, vendor=vendor).count()
    current_avg_response_time = vendor.average_response_time
    instance_response_time = (
        instance.acknowledgment_date - instance.issue_date).total_seconds() / 3600.0
    new_avg_response_time = (float(current_avg_response_time*(acknowledged_count-1)) +
                             float(instance_response_time))/acknowledged_count
    print(
        f"instance_response_time:{( instance.acknowledgment_date - instance.issue_date).total_seconds()}")
    return round(new_avg_response_time, 1)
