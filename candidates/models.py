from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.db import models
from company.models import Company
from offer.models import JobOffer
from users.models import UserAccount
from utils.base_model import BaseModel


class Candidate(BaseModel):
    STATUS = (
        ("PENDING", "PENDING"),
        ("ACCEPTED", "ACCEPTED"),
        ("REJECTED", "REJECTED"),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    future_recruitment = models.BooleanField(default=False)
    message = models.TextField(max_length=500, blank=True, null=True)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default="PENDING")
    cv = models.FileField(
        upload_to="cv",
        validators=[
            FileExtensionValidator(
                allowed_extensions=settings.ALLOWED_RESUME_FORMATS,
                message="Only PDF file is allowed"
            ),
        ],
        null=True,
        blank=True
    )

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
