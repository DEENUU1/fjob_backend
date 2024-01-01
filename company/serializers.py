from rest_framework.serializers import ModelSerializer, IntegerField

from location.serializers import AddressSerializer
from .models import Company


class CompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyEditSerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    company_id = IntegerField(write_only=True)

    class Meta:
        model = Company
        fields = '__all__'


class CompanyListSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = ["id", "name", "slug", "logo"]


class CompanyDetailsSerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = [
            "id",
            "slug",
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
