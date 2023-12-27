from rest_framework.serializers import ModelSerializer

from .models import PaymentInfo, Product


class PaymentInfoSerializer(ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ("name", "value", "price_euro")
