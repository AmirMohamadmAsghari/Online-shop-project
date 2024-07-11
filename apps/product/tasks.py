from celery import shared_task
from django.utils import timezone
from apps.product.models import Discount


@shared_task
def clear_expired_discounts():
    now = timezone.now()
    expired_discounts = Discount.objects.filter(expiration_date__lt=now)
    print(f"Found {expired_discounts.count()} expired discounts.")

    for discount in expired_discounts:
        discount.is_deleted = True
        discount.is_active = False
        discount.save()
        print(f"Discount ID {discount.id}: is_delete set to {discount.is_deleted}")