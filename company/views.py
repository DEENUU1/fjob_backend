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
from .serializers import (
    CompanySerializer,
)


class CompanyOfferListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        company = Company.objects.get(user=request.user)

        if company.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        queryset = JobOffer.objects.filter(company=company)
        serializer = JobOfferSerializer(queryset, many=True)
        return Response(serializer.data)


class CompanyOfferView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def retrieve(self, request, pk=None):
        queryset = JobOffer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
        if offer.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = JobOfferSerializer(offer)
        return Response(serializer.data)


class CompanyPublicView(ViewSet):

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
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyUserView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        company_id = request.data.get("company_id")
        company = Company.objects.get(pk=company_id)

        if company.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request):
        company_id = request.data.get("company_id")
        company = Company.objects.get(pk=company_id)

        if company.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        company.is_active = False
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
