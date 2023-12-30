from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from offer.models import (
    JobOffer,
)
from offer.serializers import (
    JobOfferSerializer
)
from .models import Company
from .permissions import IsCompanyUser
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    CompanyDetailsSerializer,
)


class CompanyOfferListView(APIView):
    # Return list of offers for the specified Company; only users to whom the company belongs can use it
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get(self, request, *args, **kwargs):
        company = get_object_or_404(Company, user=request.user)
        queryset = JobOffer.objects.filter(company=company)
        serializer = JobOfferSerializer(queryset, many=True)
        return Response(serializer.data)


class CompanyOfferView(ViewSet):
    # Return details for the specified offer for the specified Company; only users to whom the company belongs can use it
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def retrieve(self, request, pk=None):
        queryset = JobOffer.objects.all()
        offer = get_object_or_404(queryset, pk=pk, company__user=request.user)
        serializer = JobOfferSerializer(offer)
        return Response(serializer.data)


class CompanyPublicView(ViewSet):
    # Return a list and details of active Company models

    def list(self, request):
        companies = Company.objects.filter(is_active=True)
        serializer = CompanyListSerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Company.objects.filter(is_active=True)
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanyDetailsSerializer(company)
        return Response(serializer.data)


class UserCompanyView(APIView):
    # Return Company object for the specified user object
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        if not company:
            return Response({"detail": "Company not found for the user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyUserView(APIView):
    # Allow user to edit or delete Company
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def put(self, request):
        company_id = request.data.get("company_id")
        company = get_object_or_404(Company, pk=company_id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
