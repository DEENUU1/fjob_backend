from rest_framework.serializers import ModelSerializer
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
