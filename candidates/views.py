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

from django.db.models import Count
from datetime import timedelta, date
from django.utils import timezone


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
        "status",
        "future_recruitment",
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
        all_objects = candidates.count()

        return {
            "count": all_objects,
            "pending": pending_count,
            "accepted": accepted_count,
            "rejected": rejected_count,
        }

    def get(self, request, job_offer_id):
        status_count = self.get_candidate_status_count(job_offer_id)
        return Response(status_count)


class NumCandidatePerDayTimeline(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get(self, request, job_offer_id):
        candidates = Candidate.objects.filter(
            job_offer_id=job_offer_id
        )

        num_candidates_per_day = candidates.values('created_at__date').annotate(num_candidates=Count('id')).order_by(
            'created_at__date')

        start_date = num_candidates_per_day.first()['created_at__date']
        end_date = num_candidates_per_day.last()['created_at__date']
        all_dates = [start_date + timedelta(days=x) for x in range((end_date - start_date).days + 1)]

        results_dict = {entry['created_at__date']: entry['num_candidates'] for entry in num_candidates_per_day}

        # Complete empty dates
        for date in all_dates:
            if date not in results_dict:
                results_dict[date] = 0

        # Sort data
        sorted_results = [{'created_at__date': str(date), 'num_candidates': results_dict[date]} for date in
                          sorted(results_dict.keys())]

        return Response(sorted_results)