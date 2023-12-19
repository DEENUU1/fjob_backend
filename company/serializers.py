from rest_framework.serializers import ModelSerializer
from .models import Company
from location.serializers import AddressSerializer


class CompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    
    class Meta:
        model = Company
        fields = '__all__'
