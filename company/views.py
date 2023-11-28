from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Company,
)
from offer.models import (
    JobOffer,
)
from .serializers import (
    CompanySerializer,
)
from offer.serializers import (
    JobOfferSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated


class CompanyOfferView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def list(self):
        queryset = JobOffer.objects.all()
        serializer = JobOfferSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = JobOffer.objects.all()
        offer = get_object_or_404(queryset, pk=pk)
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

        serializer = JobOfferSerializer(offer, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class CompanyOfferListView(APIView):

    def get(self, request, *args, **kwargs):
        company_id = kwargs.get("company_id")
        company = Company.objects.get(pk=company_id)
        offers = JobOffer.objects.filter(company=company, is_active=True)
        serializer = JobOfferSerializer(offers, many=True)
        return Response(serializer.data)


class UserCheckCompanyView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        try:
            company = Company.objects.get(user=user)
            if company:
                return Response(status=status.HTTP_200_OK)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


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


class CompanyUserView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def retrive(self, request, pk=None):
        queryset = Company.objects.filter(user=request.user)
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def create(self, request):
        # Check if user has Company
        # In the future I'll move this code because it's going to be more complex
        # Because user will be able to pay for creating more companies
        user_companies = Company.objects.filter(user=self.request.user).count()
        if request.user.num_of_available_companies == user_companies:
            return Response(
                {"info": "You have reached the limit of Companies. Pay to make more"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def partial_update(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        company.is_active = False
        company.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
