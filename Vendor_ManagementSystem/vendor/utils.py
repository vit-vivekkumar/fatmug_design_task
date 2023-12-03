from django.db.models import Avg, Count

def update_vendor_metrics(vendor):
    completed_orders = PurchaseOrder.objects.filter(vendor=vendor, status='completed')

    vendor.on_time_delivery_rate = (completed_orders.filter(delivery_date__lte=models.F('acknowledgment_date')).count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

    vendor.quality_rating_avg = completed_orders.exclude(quality_rating__isnull=True).aggregate(Avg('quality_rating'))['quality_rating__avg'] or 0

    vendor.average_response_time = completed_orders.exclude(acknowledgment_date__isnull=True).aggregate(Avg(models.F('acknowledgment_date') - models.F('issue_date')))['acknowledgment_date__avg'].total_seconds() or 0

    vendor.fulfillment_rate = (completed_orders.filter(status='completed', quality_rating__isnull=True).count() / completed_orders.count()) * 100 if completed_orders.count() > 0 else 0

    vendor.save()
