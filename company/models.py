from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models

from company.utils.validate_file_size import validate_file_size
from location.models import Address
from users.models import UserAccount


class CompanyCategory(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Company Category"
        verbose_name_plural = "Company Categories"
        ordering = ['name']


class Company(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    category = models.ForeignKey(CompanyCategory, on_delete=models.CASCADE, null=True, blank=True)
    logo = models.FileField(
        upload_to="logo",
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.ALLOWED_IMAGE_FORMATS,
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

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Company"
        verbose_name_plural = "Companies"
