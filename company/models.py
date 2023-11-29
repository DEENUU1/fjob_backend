from django.db import models
from location.models import Address
from users.models import UserAccount


class Company(models.Model):
    name = models.CharField(max_length=255)
    # logo = # Todo implement later with s3 bucket
    company_size = models.CharField(max_length=255, default=1)
    description = models.TextField(null=True, blank=True)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    addresses = models.ManyToManyField(Address, blank=True)
    num_of_offers_to_add = models.IntegerField(default=1)
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    instagram_url = models.URLField(null=True, blank=True)
    youtube_url = models.URLField(null=True, blank=True)
    website_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

