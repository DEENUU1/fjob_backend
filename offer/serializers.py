from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from company.serializers import CompanySerializer
from location.serializers import AddressSerializer
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    Salary,
    JobOffer
)


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
        fields = '__all__'


class JobOfferHelperSerializer(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ("id", "title",)


class JobOfferSerializerCreate(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = "__all__"


class ScrapedDataSerializer(serializers.Serializer):
    title = serializers.CharField()
    description = serializers.CharField(allow_null=True, required=False)
    is_remote = serializers.BooleanField(allow_null=True, required=False)
    is_hybrid = serializers.BooleanField(allow_null=True, required=False)
    skills = serializers.CharField(allow_null=True, required=False)
    salary = serializers.ListField(child=serializers.DictField(allow_null=True, required=False))
    experience = serializers.ListField(child=serializers.CharField(allow_null=True, required=False))
    work_type = serializers.CharField(allow_null=True, required=False)
    employment_type = serializers.ListField(allow_null=True, child=serializers.CharField(required=False))
    company_logo = serializers.URLField(allow_null=True, required=False)
    url = serializers.URLField()
    company_name = serializers.CharField(allow_null=True, required=False)
    addresses = serializers.ListField(allow_null=True, child=serializers.DictField(required=False))
