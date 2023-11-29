from django.contrib import admin
from .models import Product, PaymentInfo


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "value", "price_euro"]
    list_filter = ["type"]
    list_editable = ["type", "value", "price_euro"]


class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "payment_bool", "created_at"]
    list_filter = ["user", "product"]
    list_editable = ["payment_bool"]


admin.site.register(Product, ProductAdmin)
admin.site.register(PaymentInfo, PaymentInfoAdmin)
