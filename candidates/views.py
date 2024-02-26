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
    _service = CandidateService(CandidateRepository())

    def post(self, request):
        serializer = InputCandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        candidate = self._service.create(data)
        return Response(candidate.id, status=status.HTTP_201_CREATED)


class CandidateUserListView(APIView):
    permission_classes = (IsAuthenticated, )
    _service = CandidateService(CandidateRepository())

    def get(self, request):
        user = request.user
        candidates = self._service.get_user_applications(user)
        serializer = OutputCandidateUserSerializer(candidates, many=True)
        return Response(serializer.data)


class CandidateCompanyViewSet(ViewSet):
    permission_classes = (IsAuthenticated, IsCompanyUser, )

    def partial_update(self, request, pk=None):
        # Todo move logic to service layer
        candidate = get_object_or_404(Candidate, pk=pk)
        serializer = InputCandidateCompanyUpdateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateCompanyListView(ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = OutputCandidateCompanyListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    permission_classes = (IsAuthenticated, IsCompanyUser, )
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
        job_offer_id = self.kwargs.get("job_offer_id")
        queryset = Candidate.objects.filter(job_offer__id=job_offer_id)
        return queryset


class CountCandidateStatus(APIView):
    permission_classes = (IsAuthenticated, IsCompanyUser, )
    _service = CandidateService(CandidateRepository())

    def get(self, request, job_offer_id: int):
        status_count = self._service.count_candidate_status(job_offer_id)
        return Response(status_count)


class NumCandidatePerDayTimeline(APIView):
    permission_classes = (IsAuthenticated, IsCompanyUser, )
    _service = CandidateService(CandidateRepository())

    def get(self, request, job_offer_id: int):
        sorted_result = self._service.get_candidate_timeline(job_offer_id)
        return Response(sorted_result)
