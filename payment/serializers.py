from .models import PaymentInfo, Product
from rest_framework.serializers import ModelSerializer


class PaymentInfoSerializer(ModelSerializer):
    class Meta:
        model = PaymentInfo
        fields = "__all__"


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = "__all__"

