from django.db import models
from django.utils import timezone

from location.models import Address
from company.models import Company

from datetime import timedelta


class WorkType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class EmploymentType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Experience(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Salary(models.Model):
    CURRENCIES = (
        ('PLN', 'PLN'),
        ('EURO', 'EURO'),
        ('USD', 'USD'),
    )
    SCHEDULES = (
        ('MONTHLY', 'MONTHLY'),
        ('YEARLY', 'YEARLY'),
        ('WEEKLY', 'WEEKLY'),
        ('DAILY', 'DAILY'),
        ('HOURLY', 'HOURLY'),
    )

    salary_from = models.FloatField()
    salary_to = models.FloatField()
    currency = models.CharField(max_length=10, choices=CURRENCIES)
    schedule = models.CharField(max_length=10, choices=SCHEDULES)

    def __str__(self):
        return f'{self.salary_from} - {self.salary_to} {self.currency} {self.schedule}'


class JobOffer(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=5000, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    addresses = models.ManyToManyField(Address, blank=True)
    is_remote = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    days_until_expiration = models.IntegerField(default=30)
    apply_form = models.URLField(null=True, blank=True)
    skills = models.CharField(max_length=100, null=True, blank=True)
    salary = models.ManyToManyField(Salary, blank=True)
    experience = models.ManyToManyField(Experience, blank=True)
    work_type = models.ManyToManyField(WorkType, blank=True)
    employment_type = models.ManyToManyField(EmploymentType, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_archived = models.BooleanField(default=False)

    # This fields are only used for job offers that are scraped from other websites
    # It shouldn't display for company when the user is trying to add a new offer
    company_logo = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_scraped = models.BooleanField(default=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)

    @property
    def is_new(self):
        threshold_days = 1
        return (timezone.now() - self.created_at) < timedelta(days=threshold_days)

    @property
    def is_expired(self):
        return (timezone.now() - self.created_at) < timedelta(days=self.days_until_expiration)

    @property
    def days_until_expiration_str(self):
        # Count based on days_until_expiration and created_at fields
        return self.days_until_expiration - (timezone.now() - self.created_at).days

    def __str__(self):
        return self.title

