from django.db import models
from location.models import Address
from users.models import UserAccount
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > (3 * 1024 * 1024):
        raise ValidationError(f"Max file size is 5 MB")


class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['png', 'jpg', 'jpeg'],
                message="Only png, jpg, jpeg files are allowed"
            ),
            validate_file_size
        ],
        null=True,
        blank=True
    )
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
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.name

