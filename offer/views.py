from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from company.models import Company
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
    JobOfferSerializer
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


class OfferListView(ListAPIView):
    queryset = JobOffer.objects.filter(status="ACTIVE")
    serializer_class = JobOfferSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)
    throttle_classes = [UserRateThrottle]

    # JobOffer fields by which objects can be ordered
    # Currently there is a ordering by created time (from newest/oldest) and salary (from lowest/highest)
    ordering_fields = [
        "created_at",
        # salary__salary_from should be used for - price lowest
        "salary__salary_from",
        # salary__salary_to should be used for - price highest
        "salary__salary_to",
    ]
    # Job offer fields by which objects can be searched
    # @ allows to run Full-text search, works only with PostgreSQL
    if settings.WORKING_MODE == "prod":
        search_fields = ["@title", "@description", "@skills"]
    else:
        search_fields = ["title", "description", "skills"]
    # Job offer fields by which objects can be filtered
    # Todo add filtering by city and region
    filterset_fields = [
        "is_remote",
        "is_hybrid",
        # "adresses__country",
        "experience",
        "work_type",
        "employment_type"
    ]

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class JobOfferView(ViewSet):
    lookup_field = 'slug'

    def retrieve(self, request, slug: str = None):
        queryset = JobOffer.objects.all()
        offer = get_object_or_404(queryset, slug=slug)
        serializer = JobOfferSerializer(offer)
        return Response(serializer.data)


class CompanyOfferListView(APIView):

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get("company_id")
        company = Company.objects.get(pk=company_id)
        offers = JobOffer.objects.filter(company=company, status="ACTIVE")
        serializer = JobOfferSerializer(offers, many=True)
        return Response(serializer.data)
