from django.db import models
from offer.models import JobOffer
from users.models import UserAccount


class Candidate(models.Model):
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    # address = ...
    # resume = ...
    message = models.TextField(max_length=5000, null=True, blank=True)
    url = models.URLField(null=True, blank=True)

    def __str__(self):
        return self.full_name
