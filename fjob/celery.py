from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "offer.settings")
app = Celery("fjob_backend")
app.config_from_object(settings, namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    "delete-scraped-offers-after-30-days": {
        "task": "offer.task.delete_scraped_offers_after_30_days",
        "schedule": 86400,  # Every 24H
    },
    "delete-offers-after-year": {
        "task": "offer.task.delete_offers_after_year",
        "schedule": 86400,  # Every 24H
    },
}