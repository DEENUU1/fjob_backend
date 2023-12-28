from datetime import timedelta

from django.db import models
from django.utils import timezone

from offer.models import JobOffer
from users.models import UserAccount


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

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'


class Report(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    description = models.CharField(max_length=255)
    reviewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description

    @property
    def is_new(self):
        threshold_days = 1
        return (timezone.now() - self.created_at) < timedelta(days=threshold_days)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
