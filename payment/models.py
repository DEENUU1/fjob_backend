from django.db import models
from users.models import UserAccount
from company.models import Company


class Product(models.Model):
    TYPES = (
        ("NEW_COMPANY", "NEW_COMPANY"),
        ("NEW_OFFER", "NEW_OFFER")
    )
    type = models.CharField(max_length=20, choices=TYPES)
    name = models.CharField(max_length=50)
    value = models.IntegerField(default=1)
    price_euro = models.DecimalField(max_digits=10, decimal_places=2)
    price_euro_id = models.CharField(max_length=500)

    def __str__(self):
        return f"{self.name} {self.value}"


class PaymentInfo(models.Model):
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    payment_bool = models.BooleanField(default=False)
    stripe_checkout_id = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user} {self.product} {self.payment_bool}"
