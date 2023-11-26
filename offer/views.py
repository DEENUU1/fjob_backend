from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from django_filters import rest_framework as filters
from fjob.pagination import CustomPagination
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    Salary,
    JobOffer
)
from .serializers import (
    WorkTypeSerializer,
    EmploymentTypeSerializer,
    ExperienceSerializer,
    SalarySerializer,
)


class WorkTypeView(ViewSet):

    def list(self, request):
        work_types = WorkType.objects.all()
        serializer = WorkTypeSerializer(work_types, many=True)
        return Response(serializer.data)


class EmploymentTypeView(ViewSet):

    def list(self, request):
        employment_types = EmploymentType.objects.all()
        serializer = EmploymentTypeSerializer(employment_types, many=True)
        return Response(serializer.data)


class ExperienceView(ViewSet):
    def list(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


class SalaryView(APIView):
    def get(self, requests):
        salaries = Salary.objects.all()

        if not salaries:
            return Response(status=status.HTTP_204_NO_CONTENT)

        min_salary = min(salary.salary_from for salary in salaries)
        max_salary = max(salary.salary_to for salary in salaries)

        result = {
            "min": min_salary,
            "max": max_salary,
        }

        return Response(result)
