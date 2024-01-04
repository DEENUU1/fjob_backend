from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import CreateAPIView
from company.models import Company
from fjob.pagination import CustomPagination
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


class CandidateCompanyRetrieveUpdateViewSet(ViewSet):
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def retrieve(self, request, pk=None):
        user = request.user
        company = get_object_or_404(Company, user=user)
        candidate = get_object_or_404(Candidate, pk=pk, company=company)
        serializer = CandidateCompanyListSerializer(candidate)
        return Response(serializer.data)

    def partial_update(self, request, pk=None):
        user = request.user
        company = get_object_or_404(Company, user=user)
        candidate = get_object_or_404(Candidate, pk=pk, company=company)
        serializer = CandidateCompanyUpdateSerializer(candidate, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CandidateCompanyListView(APIView):
    queryset = Candidate.objects.all()
    serializer_class = CandidateCompanyListSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter)

    # Order by created time
    ordering_fields = [
        "created_at",
    ]

    # Filter candidates by status
    filterset_fields = [
        "status"
    ]

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)
