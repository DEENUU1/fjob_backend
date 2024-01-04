from django.db import models
from company.models import Company
from offer.models import JobOffer
from users.models import UserAccount


class Candidate(models.Model):
    STATUS = (
        ("PENDING", "PENDING"),
        ("ACCEPTED", "ACCEPTED"),
        ("REJECTED", "REJECTED"),
    )

    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField(max_length=500, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    job_offer = models.ForeignKey(JobOffer, on_delete=models.CASCADE)
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE, blank=True, null=True)
    status = models.CharField(max_length=10,  choices=STATUS, default="PENDING")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Candidate"
        verbose_name_plural = "Candidates"
