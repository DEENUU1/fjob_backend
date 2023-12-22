from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

from location.models import Address
from offer.models import JobOffer
from users.models import UserAccount


def validate_file_size(value):
    filesize = value.size

    if filesize > (5 * 1024 * 1024):
        raise ValidationError(f"Max file size is 5 MB")


class Candidate(models.Model):
    STATUS = (
        ("Pending", "Pending"),
        ("Reviewed", "Reviewed"),
        ("Rejected", "Rejected"),
    )
    full_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=True, blank=True)
    offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    address = models.ManyToManyField(Address, blank=True)
    resume = models.FileField(
        validators=[
            FileExtensionValidator(
                allowed_extensions=['pdf'],
                message="Only PDF files are allowed"
            ),
            validate_file_size,
        ],
        blank=True,
    )
    message = models.TextField(max_length=5000, null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS, default="Pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Candidate'
        verbose_name_plural = 'Candidates'
