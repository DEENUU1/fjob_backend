from rest_framework.serializers import ModelSerializer

from location.serializers import AddressSerializer
from .models import Company


class CompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'
