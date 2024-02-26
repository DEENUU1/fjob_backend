from rest_framework.serializers import ModelSerializer, IntegerField

from location.serializers import AddressSerializer
from .models import Company, CompanyCategory


class OutputCompanyCategorySerializer(ModelSerializer):
    class Meta:
        model = CompanyCategory
        fields = "__all__"


class OutputCompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    category = OutputCompanyCategorySerializer()

    class Meta:
        model = Company
        fields = '__all__'


class InputCompanyEditSerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    company_id = IntegerField(write_only=True)

    class Meta:
        model = Company
        fields = [
            "company_id",
            "name",
            "category",
            "logo",
            "company_size",
            "description",
            "addresses",
            "linkedin_url",
            "facebook_url",
            "twitter_url",
            "instagram_url",
            "youtube_url",
            "is_active"
        ]


class OutputCompanyListSerializer(ModelSerializer):
    category = OutputCompanyCategorySerializer()

    class Meta:
        model = Company
        fields = [
            "id",
            "name",
            "slug",
            "logo",
            "category"
        ]


class OutputCompanyDetailsSerializer(ModelSerializer):
    category = OutputCompanyCategorySerializer()

    class Meta:
        model = Company
        fields = [
            "id",
            "slug",
            "name",
            "category",
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
