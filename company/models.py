from django.db import models
from location.models import Address
from users.models import UserAccount


class Company(models.Model):
    name = models.CharField(max_length=255)
    # logo = # Todo implement later with s3 bucket
    company_size = models.CharField(max_length=255, default=1)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
