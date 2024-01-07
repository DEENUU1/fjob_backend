import random
import string
from datetime import timedelta

from django.db import models
from django.utils import timezone

from company.models import Company
from location.models import Address


class WorkType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Work Type'
        verbose_name_plural = 'Work Types'


class EmploymentType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Employment Type'
        verbose_name_plural = 'Employment Types'


class Experience(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-name']
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'


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

    salary_from = models.FloatField(null=True, blank=True)
    salary_to = models.FloatField(null=True, blank=True)
    currency = models.CharField(max_length=10, choices=CURRENCIES, null=True, blank=True)
    schedule = models.CharField(max_length=10, choices=SCHEDULES, null=True, blank=True)

    def __str__(self):
        return f'{self.salary_from} - {self.salary_to} {self.currency} {self.schedule}'

    class Meta:
        ordering = ['-salary_from']
        verbose_name = 'Salary'
        verbose_name_plural = 'Salaries'


class JobOffer(models.Model):
    STATUS = (
        ("DRAFT", "DRAFT"),
        ("PENDING", "PENDING"),
        ("ACTIVE", "ACTIVE"),
        ("EXPIRED", "EXPIRED"),
    )

    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(max_length=5000, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True)
    addresses = models.ManyToManyField(Address, blank=True)
    is_remote = models.BooleanField(default=False)
    is_hybrid = models.BooleanField(default=False)
    days_until_expiration = models.IntegerField(default=30)
    apply_form = models.URLField(null=True, blank=True, default=None)
    skills = models.CharField(max_length=100, null=True, blank=True)
    salary = models.ManyToManyField(Salary, blank=True)
    experience = models.ManyToManyField(Experience, blank=True)
    work_type = models.ManyToManyField(WorkType, blank=True)
    employment_type = models.ManyToManyField(EmploymentType, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS, default="DRAFT")

    # These fields are only used for job offers that are scraped from other websites
    # It shouldn't display for company when the user is trying to add a new offer
    company_logo = models.URLField(null=True, blank=True)
    url = models.URLField(null=True, blank=True)
    is_scraped = models.BooleanField(default=True)
    company_name = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Job Offer"
        verbose_name_plural = "Job Offers"

    @property
    def is_new(self) -> bool:
        threshold_days = 1
        return (timezone.now() - self.created_at) < timedelta(days=threshold_days)

    @property
    def is_expired(self) -> bool:
        return (timezone.now() - self.created_at) >= timedelta(days=self.days_until_expiration)

    @property
    def days_until_expiration_str(self) -> str:
        return str(self.days_until_expiration - (timezone.now() - self.created_at).days)

    def __str__(self) -> str:
        return self.title
