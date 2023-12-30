from rest_framework.serializers import ModelSerializer

from location.serializers import AddressSerializer
from .models import Company


class CompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "logo"]


class CompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "logo",
            "company_size",
            "description",
            "addresses",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "youtube_url",
            "website_url"
        ]
