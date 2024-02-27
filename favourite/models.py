from django.db import models

from offer.models import JobOffer
from users.models import UserAccount
from utils.base_model import BaseModel


class Favourite(BaseModel):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} {self.offer}"

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Favourite"
        verbose_name_plural = "Favourites"
