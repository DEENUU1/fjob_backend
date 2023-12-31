from django.contrib import admin

from .models import Product, PaymentInfo


class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", "type", "value", "price_euro"]
    list_filter = ["type"]


class PaymentInfoAdmin(admin.ModelAdmin):
    list_display = ["user", "product", "payment_bool", "created_at"]
    list_filter = ["product"]


admin.site.register(Product, ProductAdmin)
admin.site.register(PaymentInfo, PaymentInfoAdmin)
