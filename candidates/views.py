from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from rest_framework import status
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from company.permissions import IsCompanyUser
from fjob.pagination import CustomPagination
from .models import Candidate
from .repository.candidate_repository import CandidateRepository
from .serializers import (
    OutputCandidateCompanyListSerializer,
    InputCandidateSerializer,
    OutputCandidateUserSerializer,
    InputCandidateCompanyUpdateSerializer
)
from .services.candidate import CandidateService


class CandidateCreateAPIView(APIView):
    """
    API view for creating a new Candidate.

    Attributes:
    - _service: An instance of CandidateService for handling candidate-related operations.

    Methods:
    - post(self, request): Handles POST requests to create a new candidate.
    """

    _service = CandidateService(CandidateRepository())

    def post(self, request):
        """
        Handles POST requests to create a new candidate.

        Parameters:
        - request: The HTTP request object containing candidate data.

        Returns:
        - Response: A response with the ID of the created candidate and HTTP status code 201.
        """
        serializer = InputCandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        candidate = self._service.create(data)
        return Response(candidate.id, status=status.HTTP_201_CREATED)


class CandidateUserListView(APIView):
    """
    API view for retrieving a list of candidates associated with the currently authenticated user.

    Attributes:
    - _service: An instance of CandidateService for handling candidate-related operations.

    Methods:
    - get(self, request): Handles GET requests to retrieve user-related candidate information.
    """

    permission_classes = (IsAuthenticated,)
    _service = CandidateService(CandidateRepository())

    def get(self, request):
        """
        Handles GET requests to retrieve user-related candidate information.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: A response with serialized candidate data for the authenticated user.
        """
        user = request.user
        candidates = self._service.get_user_applications(user)
        serializer = OutputCandidateUserSerializer(candidates, many=True)
        return Response(serializer.data)


class CandidateCompanyViewSet(ViewSet):
    """
    ViewSet for performing partial updates on Candidate objects for company users.

    Attributes:
    - permission_classes: Permission classes for restricting access.

    Methods:
    - partial_update(self, request, pk=None): Handles partial updates for a specific Candidate object.
    """

    permission_classes = (IsAuthenticated, IsCompanyUser,)

    def partial_update(self, request, pk=None):
        """
        Handles partial updates for a specific Candidate object.

        Parameters:
        - request: The HTTP request object.
        - pk: The primary key of the candidate to be updated.

        Returns:
        - Response: A response with the updated candidate data or errors.
        """
        # Todo move logic to service layer
        candidate = get_object_or_404(Candidate, pk=pk)
        serializer = InputCandidateCompanyUpdateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateCompanyListView(ListAPIView):
    """
    ListAPIView for retrieving a list of candidates associated with a specific job offer for company users.

    Attributes:
    - queryset: The queryset of Candidate objects.
    - serializer_class: The serializer class for candidate data.
    - filter_backends: The filter backends for handling queries.
    - permission_classes: Permission classes for restricting access.
    - pagination_class: The pagination class for paginating results.
    - ordering_fields: The fields for ordering the queryset.
    - filterset_fields: The fields for filtering the queryset.

    Methods:
    - get_queryset(self, *args, **kwargs): Overrides the default queryset to filter candidates by job offer.
    """

    queryset = Candidate.objects.all()
    serializer_class = OutputCandidateCompanyListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    permission_classes = (IsAuthenticated, IsCompanyUser,)
    pagination_class = CustomPagination

    # Order by created time
    ordering_fields = [
        "created_at",
    ]

    # Filter candidates by status
    filterset_fields = [
        "status",
        "future_recruitment",
    ]

    def get_queryset(self, *args, **kwargs):
        """
        Overrides the default queryset to filter candidates by job offer.

        Returns:
        - QuerySet: The filtered queryset of candidates.
        """
        job_offer_id = self.kwargs.get("job_offer_id")
        queryset = Candidate.objects.filter(job_offer__id=job_offer_id)
        return queryset


class CountCandidateStatus(APIView):
    """
    API view for retrieving the count of candidates with different statuses for a specific job offer.

    Attributes:
    - permission_classes: Permission classes for restricting access.
    - _service: An instance of CandidateService for handling candidate-related operations.

    Methods:
    - get(self, request, job_offer_id: int): Handles GET requests to retrieve candidate status counts.
    """

    permission_classes = (IsAuthenticated, IsCompanyUser,)
    _service = CandidateService(CandidateRepository())

    def get(self, request, job_offer_id: int):
        """
        Handles GET requests to retrieve candidate status counts for a specific job offer.

        Parameters:
        - request: The HTTP request object.
        - job_offer_id: The ID of the job offer.

        Returns:
        - Response: A response with a dictionary containing candidate status counts.
        """
        status_count = self._service.count_candidate_status(job_offer_id)
        return Response(status_count)


class NumCandidatePerDayTimeline(APIView):
    """
    API view for retrieving the timeline of candidate creation for a specific job offer.

    Attributes:
    - permission_classes: Permission classes for restricting access.
    - _service: An instance of CandidateService for handling candidate-related operations.

    Methods:
    - get(self, request, job_offer_id: int): Handles GET requests to retrieve candidate creation timeline.
    """

    permission_classes = (IsAuthenticated, IsCompanyUser,)
    _service = CandidateService(CandidateRepository())

    def get(self, request, job_offer_id: int):
        """
        Handles GET requests to retrieve the timeline of candidate creation for a specific job offer.

        Parameters:
        - request: The HTTP request object.
        - job_offer_id: The ID of the job offer.

        Returns:
        - Response: A response with a list of dictionaries containing dates and the corresponding number of candidates created.
        """
        sorted_result = self._service.get_candidate_timeline(job_offer_id)
        return Response(sorted_result)
