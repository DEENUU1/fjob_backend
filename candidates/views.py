from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView, ListAPIView
from .models import Candidate
from .serializers import (
    CandidateCompanyListSerializer,
    CandidateCreateSerializer,
    CandidateUserSerializer,
    CandidateCompanyUpdateSerializer
)
from company.permissions import IsCompanyUser
from rest_framework.filters import OrderingFilter
from django_filters import rest_framework as filters
from fjob.pagination import CustomPagination


class CandidateCreateView(CreateAPIView):
    # Apply form
    serializer_class = CandidateCreateSerializer


class CandidateUserListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        candidates = Candidate.objects.filter(user=user)
        serializer = CandidateUserSerializer(candidates, many=True)
        return Response(serializer.data)


class CandidateCompanyViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def partial_update(self, request, pk=None):
        candidate = get_object_or_404(Candidate, pk=pk)
        serializer = CandidateCompanyUpdateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateCompanyListView(ListAPIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateCompanyListSerializer
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)
    permission_classes = [IsAuthenticated, IsCompanyUser]
    pagination_class = CustomPagination

    # Order by created time
    ordering_fields = [
        "created_at",
    ]

    # Filter candidates by status
    filterset_fields = [
        "status"
    ]

    def get_queryset(self, *args, **kwargs):
        job_offer_id = self.kwargs.get("job_offer_id")
        queryset = Candidate.objects.filter(job_offer__id=job_offer_id)
        return queryset


class CountCandidateStatus(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get_candidate_status_count(self, job_offer_id):
        candidates = Candidate.objects.filter(
            job_offer_id=job_offer_id
        )
        pending_count = candidates.filter(status="PENDING").count()
        accepted_count = candidates.filter(status="ACCEPTED").count()
        rejected_count = candidates.filter(status="REJECTED").count()

        return {
            "PENDING": pending_count,
            "ACCEPTED": accepted_count,
            "REJECTED": rejected_count,
        }

    def get(self, request, job_offer_id):
        status_count = self.get_candidate_status_count(job_offer_id)
        return Response(status_count)
