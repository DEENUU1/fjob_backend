from django.db import models

from offer.models import JobOffer
from users.models import UserAccount


class Favourite(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.offer}"
