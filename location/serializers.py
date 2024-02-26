from rest_framework.serializers import ModelSerializer

from .models import (
    Address,
    City,
    Region,
    Country
)


class OutputCountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = '__all__'


class OutputRegionSerializer(ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class OutputCitySerializer(ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class OutputAddressSerializer(ModelSerializer):
    country = OutputCountrySerializer()
    city = OutputCitySerializer()
    region = OutputRegionSerializer()

    class Meta:
        model = Address
        fields = '__all__'
