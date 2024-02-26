from django.conf import settings
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from company.models import Company
from company.permissions import IsCompanyUser
from fjob.pagination import CustomPagination
from offer.rate_throttle import JobOfferRateAnonThrottle, JobOfferRateUserThrottle
from offer.repository.offer_rate_repository import JobOfferRateRepository
from offer.repository.offer_repository import OfferRepository
from offer.repository.salary_repository import SalaryRepository
from offer.services.offer import OfferService
from offer.services.offer_rate import OfferRateService
from offer.services.salary import SalaryService
from .models import (
    WorkType,
    EmploymentType,
    Experience,
    JobOffer,
)
from .serializers import (
    WorkTypeSerializer,
    EmploymentTypeSerializer,
    ExperienceSerializer,
    JobOfferSerializer,
    JobOfferSerializerCreate,
    ScrapedDataSerializer,
    JobOfferCompanySerializer,
    JobOfferRateCreateSerializer,
    JobOfferSerializerUpdate
)


class WorkTypeListAPIView(ListAPIView):
    """
    ListAPIView to retrieve a list of WorkType objects.
    """
    queryset = WorkType.objects.all()
    serializer_class = WorkTypeSerializer


class EmploymentTypeListAPIView(ListAPIView):
    """
    ListAPIView to retrieve a list of EmploymentType objects.
    """
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer


class ExperienceListAPIView(ListAPIView):
    """
    ListAPIView to retrieve a list of Experience objects.
    """
    queryset = Experience.objects.all()
    serializer_class = ExperienceSerializer


class SalaryView(APIView):
    """
    API endpoint to retrieve minimum and maximum salary information.
    """

    _service = SalaryService(SalaryRepository())

    def get(self, request):
        """
        Retrieve and return minimum and maximum salary information.
        """
        result = self._service.return_min_max_salary()
        return Response(result)


class OfferListView(ListAPIView):
    """
    ListAPIView to retrieve a paginated list of active Job Offers with various filtering and sorting options.
    """

    queryset = JobOffer.objects.filter(
        status="ACTIVE",
    )
    serializer_class = JobOfferSerializer
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    throttle_classes = (UserRateThrottle,)

    # JobOffer fields by which objects can be ordered
    # Currently there is ordering by created time (from newest/oldest) and salary (from lowest/highest)
    ordering_fields = [
        "created_at",
        # salary__salary_from should be used for - price lowest
        "salary__salary_from",
        # salary__salary_to should be used for - price highest
        "salary__salary_to",
    ]
    # Job offer fields by which objects can be searched
    # @ allows Full-text search, works only with PostgreSQL
    if settings.WORKING_MODE == "prod":
        search_fields = ["@title", "@description", "@skills"]
    else:
        search_fields = ["title", "description", "skills"]
    # Job offer fields by which objects can be filtered
    # Todo: add filtering by city and region
    filterset_fields = [
        "is_remote",
        "is_hybrid",
        # "adresses__country",
        "experience",
        "work_type",
        "employment_type"
    ]

    def get(self, request, *args, **kwargs):
        """
        Retrieve and return a paginated list of active Job Offers with applied filters and sorting.
        """
        return super().get(request, *args, **kwargs)


class JobOfferRetrieveAPIView(RetrieveAPIView):
    """
    RetrieveAPIView to get details for a specific Job Offer based on its slug.
    """
    lookup_field = 'slug'
    queryset = JobOffer.objects.filter(status="ACTIVE")
    serializer_class = JobOfferSerializer
    throttle_classes = (UserRateThrottle,)


class CompanyPublicOfferListView(ListAPIView):
    """
    ListAPIView to get a list of Job Offers (with status "ACTIVE") for a specified Company.
    """
    serializer_class = JobOfferSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Get the queryset of Job Offers with status "ACTIVE" for the specified Company.
        """
        # Get company_id from URL param
        company_id = self.kwargs.get("slug")
        company = get_object_or_404(Company, slug=company_id)
        # Filter offers with status "ACTIVE" for the specified company
        return JobOffer.objects.filter(company=company, status="ACTIVE")

    def list(self, request, *args, **kwargs):
        """
        List Job Offers with status "ACTIVE" for the specified Company.
        """
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class OfferPrivateCompanyViewSet(ViewSet):
    """
    A set of endpoints for the Company to manage Job Offers, including creation, update, and deletion.
    """

    permission_classes = (IsAuthenticated, IsCompanyUser,)

    def list(self, request):
        """
        Retrieve a list of Job Offers associated with the authenticated Company.
        """
        company = get_object_or_404(Company, user=request.user)
        queryset = JobOffer.objects.filter(company=company)
        serializer = JobOfferCompanySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        """
        Create a new Job Offer for the authenticated Company.
        """
        serializer = JobOfferSerializerCreate(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        """
        Update an existing Job Offer for the authenticated Company.
        """
        offer = get_object_or_404(JobOffer, pk=pk)

        if offer.is_expired:
            return Response(
                {"info": "Offer is expired"}, status=status.HTTP_400_BAD_REQUEST
            )

        serializer = JobOfferSerializerUpdate(offer, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        """
        Delete an existing Job Offer for the authenticated Company.
        """
        offer = get_object_or_404(JobOffer, pk=pk)
        offer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ScrapedDataView(APIView):
    """
    API endpoint to handle the saving of scraped data for Job Offers.
    Requires Token Authentication for access.
    """

    authentication_classes = [TokenAuthentication]
    permission_classes = (IsAuthenticated,)
    _service = OfferService(OfferRepository())

    def post(self, request, *args, **kwargs):
        """
        Save scraped data for multiple Job Offers.
        """
        serializer = ScrapedDataSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        self._service.save_scraped_offers(serializer.validated_data)
        return Response({"message": "Data saved successfully"}, status=status.HTTP_201_CREATED)


class JobOfferRateCreateAPIView(CreateAPIView):
    """
    CreateAPIView for submitting ratings for Job Offers.
    """
    serializer_class = JobOfferRateCreateSerializer
    throttle_classes = (JobOfferRateAnonThrottle, JobOfferRateUserThrottle,)


class JobOfferRateStatsAPIView(APIView):
    """
    API endpoint to retrieve statistics for Job Offer ratings.
    """

    _service = OfferRateService(JobOfferRateRepository())

    def get(self, request, slug: str):
        """
        Retrieve statistics for a specific Job Offer based on its slug.
        """
        result = self._service.get_offer_rate_details(slug)
        return Response(result)
