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
)


class CompanyOfferListView(APIView):
    # Return list of offer for specified Company, only users for whom company belongs can use it
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user=request.user)
        queryset = JobOffer.objects.filter(company=company)
        serializer = JobOfferSerializer(queryset, many=True)
        return Response(serializer.data)


class CompanyOfferView(ViewSet):
    # Return details for specified offer for specified Company, only users for whom company belongs can use it
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def retrieve(self, request, pk=None):
        queryset = JobOffer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        serializer = JobOfferSerializer(offer)
        return Response(serializer.data)


class CompanyPublicView(ViewSet):
    # Return list and details of Company models

    def list(self, request):
        companies = Company.objects.filter(is_active=True)
        serializer = CompanySerializer(companies, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Company.objects.filter(is_active=True)
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)


class UserCompanyView(APIView):
    # Return Company object for specified user object
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyUserView(APIView):
    # Allow user to edit or delete Company
    permission_classes = [IsAuthenticated, IsCompanyUser]

    def put(self, request):
        company_id = request.data.get("company_id")
        company = Company.objects.get(pk=company_id)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        company_id = request.data.get("company_id")
        company = Company.objects.get(pk=company_id)
        company.is_active = False
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
