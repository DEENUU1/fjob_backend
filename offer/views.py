from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
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


class WorkTypeListAPIView(ListAPIView):
    # Return list of WorkType objects
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class EmploymentTypeListAPIView(ListAPIView):
    # Return list of EmploymentType objects
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer


class ExperienceListAPIView(ListAPIView):
    # Return list of Experience objects
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


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

    queryset = JobOffer.objects.filter(status="ACTIVE", is_expired=False)
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


class JobOfferRetrieveAPIView(RetrieveAPIView):
    # Return details for specified JobOffer based on slug
    lookup_field = 'slug'
    queryset = JobOffer.objects.filter(status="ACTIVE")
    serializer_class = JobOfferSerializer
    throttle_classes = [UserRateThrottle]


class CompanyPublicOfferListView(ListAPIView):
    # Return list of offer (with status "ACTIVE") for specified Company
    serializer_class = JobOfferSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        # Get company_id from URL param
        company_id = self.kwargs.get("slug")
        company = get_object_or_404(Company, slug=company_id)
        # Filter offers with status "ACTIVE" for the specified company
        return JobOffer.objects.filter(company=company, status="ACTIVE")

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfferPrivateCompanyViewSet(ViewSet):
    # Set of endpoints for Company to create, update and delete JobOffer
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def list(self, request):
        company = get_object_or_404(Company, user=request.user)
        queryset = JobOffer.objects.filter(company=company)
        serializer = JobOfferSerializer(queryset, many=True)
        return Response(serializer.data)

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
