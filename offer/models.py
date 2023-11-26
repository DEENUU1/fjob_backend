from django.db import models
from location.models import Address


class WorkType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class EmploymentType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Experience(models.Model):
    name = models.CharField(max_length=50)

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

