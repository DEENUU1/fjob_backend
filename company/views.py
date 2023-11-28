from rest_framework.viewsets import ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Company,
)
from .serializers import (
    CompanySerializer,
)
from django.shortcuts import get_object_or_404


class UserCheckCompanyView(ViewSet):
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

    def retrive(self, request, pk=None):
        queryset = Company.objects.filter(user=request.user)
        company = get_object_or_404(queryset, pk=pk)
        serializer = CompanySerializer(company)
        return Response(serializer.data)

    def create(self, request):
        serializer = CompanySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None):
        company = Company.objects.get(pk=pk)
        serializer = CompanySerializer(company, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

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
