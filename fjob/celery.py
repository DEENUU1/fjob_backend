from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fjob.settings")
app = Celery("fjob")
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
    "delete-contact-after-year": {
        "task": "support.task.delete_contact_after_year",
        "schedule": 86400,  # Every 24H
    },
    "delete-report-after-year": {
        "task": "support.task.delete_report_after_year",
        "schedule": 86400,  # Every 24H
    }
}