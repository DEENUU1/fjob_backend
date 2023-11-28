from django.db import models
from users.models import UserAccount
from offer.models import JobOffer
from django.utils import timezone
from datetime import timedelta


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
