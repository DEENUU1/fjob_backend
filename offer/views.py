from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.authentication import TokenAuthentication
from company.models import Company
from company.permissions import IsCompanyUser
from fjob.pagination import CustomPagination
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    Salary,
    JobOffer
)
from .save_scraped import save_scraped
from .serializers import (
    WorkTypeSerializer,
    EmploymentTypeSerializer,
    ExperienceSerializer,
    JobOfferSerializer,
    JobOfferSerializerCreate,
    ScrapedDataSerializer,
)


class WorkTypeView(ViewSet):
    # Return list of WorkType

    def list(self, request):
        work_types = WorkType.objects.all()
        serializer = WorkTypeSerializer(work_types, many=True)
        return Response(serializer.data)


class EmploymentTypeView(ViewSet):
    # Return list of EmploymentType

    def list(self, request):
        employment_types = EmploymentType.objects.all()
        serializer = EmploymentTypeSerializer(employment_types, many=True)
        return Response(serializer.data)


class ExperienceView(ViewSet):
    # Return list of Experience

    def list(self, request):
        experiences = Experience.objects.all()
        serializer = ExperienceSerializer(experiences, many=True)
        return Response(serializer.data)


class SalaryView(APIView):
    # Return lowest and highest salary

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
    # Return list of JobOffer with status "ACTIVE"

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
    # Return details for specified JobOffer based on slug
    lookup_field = 'slug'

    def retrieve(self, request, slug: str = None):
        queryset = JobOffer.objects.filter(status="ACTIVE")
        offer = get_object_or_404(queryset, slug=slug)
        serializer = JobOfferSerializer(offer)
        return Response(serializer.data)


class CompanyOfferListView(APIView):
    # Return list of offer (with status "ACTIVE") for specified Company
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        # Get company_id from url param
        company_id = kwargs.get("slug")
        company = get_object_or_404(Company, pk=company_id)
        offers = JobOffer.objects.filter(company=company, status="ACTIVE")
        serializer = JobOfferSerializer(offers, many=True)
        return Response(serializer.data)


class OfferViewSet(ViewSet):
    # Set of endpoints for Company to create, update and delete JobOffer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def create(self, request):
        serializer = JobOfferSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        offer = get_object_or_404(JobOffer, pk=pk)

        if offer.is_expired:
            return Response(
                {"info": "Offer is expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = JobOfferSerializerCreate(offer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        offer = get_object_or_404(JobOffer, pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScrapedDataView(APIView):
    # Endpoint which allows to POST scraped data and save to database
    # It's a bridge between Lambda functions and Google Cloud SQL
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = ScrapedDataSerializer(data=request.data, many=True)

        if serializer.is_valid():
            data = serializer.validated_data
            for item in data:
                save_scraped(item)

            return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
