from rest_framework.serializers import ModelSerializer
from .models import (
    Address,
    City,
    Region,
    Country
)


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class RegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class CitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class AddressSerializer(ModelSerializer):
    country = CountrySerializer()
    city = CitySerializer()
    region = RegionSerializer()

    class Meta:
        model = Address
        fields = '__all__'
