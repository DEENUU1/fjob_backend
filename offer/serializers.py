from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.serializers import CompanySerializer
from location.serializers import AddressSerializer
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    Salary,
    JobOffer,
    JobOfferRate,
)
from django.db.models import Avg


class WorkTypeSerializer(ModelSerializer):
    class Meta:
        model = WorkType
        fields = '__all__'


class EmploymentTypeSerializer(ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = '__all__'


class ExperienceSerializer(ModelSerializer):
    class Meta:
        model = Experience
        fields = '__all__'


class SalarySerializer(ModelSerializer):
    class Meta:
        model = Salary
        fields = '__all__'


class JobOfferSerializer(ModelSerializer):
    salary = SalarySerializer(many=True)
    experience = ExperienceSerializer(many=True)
    work_type = WorkTypeSerializer(many=True)
    employment_type = EmploymentTypeSerializer(many=True)
    company = CompanySerializer()
    addresses = AddressSerializer(many=True)
    is_new = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    days_until_expiration_str = serializers.ReadOnlyField()

    class Meta:
        model = JobOffer
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "company",
            "addresses",
            "is_remote",
            "is_hybrid",
            "apply_form",
            "skills",
            "salary",
            "experience",
            "work_type",
            "employment_type",
            "created_at",
            "status",
            "company_logo",
            "url",
            "is_scraped",
            "company_name",
            "days_until_expiration_str",
            "is_expired",
            "is_new",
        ]


class JobOfferCompanySerializer(ModelSerializer):
    salary = SalarySerializer(many=True)
    experience = ExperienceSerializer(many=True)
    work_type = WorkTypeSerializer(many=True)
    employment_type = EmploymentTypeSerializer(many=True)
    company = CompanySerializer()
    addresses = AddressSerializer(many=True)
    is_new = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()
    days_until_expiration_str = serializers.ReadOnlyField()
    candidate_count = serializers.SerializerMethodField()
    avg_rate = serializers.SerializerMethodField()

    class Meta:
        model = JobOffer
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "company",
            "addresses",
            "is_remote",
            "is_hybrid",
            "apply_form",
            "skills",
            "salary",
            "experience",
            "work_type",
            "employment_type",
            "created_at",
            "status",
            "company_logo",
            "url",
            "is_scraped",
            "company_name",
            "days_until_expiration_str",
            "is_expired",
            "is_new",
            "candidate_count",
            "avg_rate",
        ]

    def get_candidate_count(self, obj):
        return obj.candidate_set.count()

    def get_avg_rate(self, obj):
        avg_rating = obj.jobofferrate_set.aggregate(Avg('rate'))['rate__avg']
        if avg_rating:
            return round(avg_rating, 2)
        else:
            return None


class JobOfferHelperSerializer(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ["id", "title", "slug"]


class JobOfferSerializerCreate(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = [
            "id",
            "title",
            "description",
            "company",
            "addresses",
            "is_remote",
            "is_hybrid",
            "apply_form",
            "skills",
            "salary",
            "experience",
            "work_type",
            "employment_type",
            "status",
            "days_until_expiration",
            "is_expired",
            "is_new",
        ]

    def validate_company(self, value):
        if value.num_of_offers_to_add <= 0:
            raise serializers.ValidationError("You have reached the limit of offers.")
        return value


class ScrapedDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    is_remote = serializers.BooleanField(allow_null=True, required=False)
    is_hybrid = serializers.BooleanField(allow_null=True, required=False)
    skills = serializers.CharField(allow_null=True, required=False)
    salary = serializers.ListField(child=serializers.DictField(allow_null=True, required=False))
    experience = serializers.ListField(child=serializers.CharField(allow_null=True, required=False))
    work_type = serializers.ListField(allow_null=True, child=serializers.CharField(required=False))
    employment_type = serializers.ListField(allow_null=True, child=serializers.CharField(required=False))
    company_logo = serializers.URLField(allow_null=True, required=False)
    url = serializers.URLField()
    company_name = serializers.CharField(allow_null=True, required=False)
    addresses = serializers.ListField(allow_null=True, child=serializers.DictField(required=False))


class JobOfferRateCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobOfferRate
        fields = ["rate", "job_offer"]
