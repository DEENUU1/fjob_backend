from django.db import models
from users.models import UserAccount
from company.models import Company


class UserPayment(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.payment_bool}"


class Package(models.Model):
    name = models.CharField(max_length=100)
    price_pln = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id_pln = models.CharField(max_length=500)
    price_euro = models.DecimalField(max_digits=10, decimal_places=2)
    stripe_price_id_euro = models.CharField(max_length=500)
    has_bumps = models.BooleanField(default=False)
    num_of_bumps = models.IntegerField(default=0)
    num_of_days_available = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class PackagePurchase(models.Model):
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.company} {self.package} {self.is_available}"
