# config/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# Periodic task configuration
app.conf.beat_schedule = {
    'clear-expired-discounts-every-day': {
        'task': 'apps.product.tasks.clear_expired_discounts',
        'schedule': crontab(hour=0, minute=0),  # Every day at midnight
    },
}
app.conf.timezone = 'UTC'
