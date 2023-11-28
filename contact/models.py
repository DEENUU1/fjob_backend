from django.db import models
from django.utils import timezone
from datetime import timedelta


class Contact(models.Model):
    subject = models.CharField(max_length=50)
    message = models.TextField(max_length=500)
    email = models.EmailField()
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject

    @property
    def is_new(self):
        threshold_days = 1
        return (timezone.now() - self.created_at) < timedelta(days=threshold_days)

    @property
    def is_expired(self):
        threshold_days = 90
        return (timezone.now() - self.created_at) > timedelta(days=threshold_days)
