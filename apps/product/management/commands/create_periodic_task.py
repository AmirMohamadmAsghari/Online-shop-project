from django.core.management.base import BaseCommand
from django_celery_beat.models import PeriodicTask, CrontabSchedule
from django.utils.timezone import now


class Command(BaseCommand):
    help = 'Create a periodic task to clear expired discounts'

    def handle(self, *args, **kwargs):
        schedule, created = CrontabSchedule.objects.get_or_create(
            minute='0',
            hour='0',
            day_of_week='*',
            day_of_month='*',
            month_of_year='*',
        )

        PeriodicTask.objects.create(
            crontab=schedule,
            name='Clear expired discounts daily at midnight',
            task='apps.product.tasks.clear_expired_discounts',
            start_time=now()
        )

        self.stdout.write(self.style.SUCCESS('Successfully created periodic task'))
