from rest_framework.serializers import ModelSerializer, IntegerField

from location.serializers import AddressSerializer
from .models import Company, CompanyCategory


class CompanyCategorySerializer(ModelSerializer):
    class Meta:
        model = CompanyCategory
        fields = "__all__"


class CompanySerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    category = CompanyCategorySerializer()

    class Meta:
        model = Company
        fields = '__all__'


class CompanyEditSerializer(ModelSerializer):
    addresses = AddressSerializer(many=True)
    company_id = IntegerField(write_only=True)
    category = CompanyCategorySerializer()

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


class CompanyListSerializer(ModelSerializer):
    category = CompanyCategorySerializer()

    class Meta:
        model = Company
        fields = ["id", "name", "slug", "logo", "category"]


class CompanyDetailsSerializer(ModelSerializer):
    category = CompanyCategorySerializer()

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
