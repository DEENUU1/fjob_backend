from rest_framework.serializers import ModelSerializer

from .models import Product


class OutputProductListSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ["id", "name", "value", "price_euro"]
