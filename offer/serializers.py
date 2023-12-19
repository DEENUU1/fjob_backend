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
