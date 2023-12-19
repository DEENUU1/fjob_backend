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

    def create(self, request):
        company_id = request.data.get("company_id")
        if company_id is None:
            return Response({"info": "You need to select Company"}, status=status.HTTP_400_BAD_REQUEST)

        company = Company.objects.get(pk=company_id)
        if company:
            if company.num_of_offers_to_add > 0:
                serializer = JobOfferSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()

                company.num_of_offers_to_add -= 1
                company.save()

                return Response(serializer.data, status=status.HTTP_201_CREATED)

            else:
                return Response({"info": "You have reached the limit of offers"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"info": "Company does not exists"}, status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request, pk=None):
        offer = JobOffer.objects.get(pk=pk)

        if offer.is_expired:
            return Response({"info": "Offer is expired"}, status=status.HTTP_400_BAD_REQUEST)

        new_status = request.data.get("status", None)
        if new_status and offer.status == "EXPIRED":
            return Response(
                {
                    "info": "You can't change the status for this job offer, it's already expired"
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = JobOfferSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
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


class CompanyUserView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def partial_update(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        if company.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        if company.user != self.request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        company.is_active = False
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
