from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company, CompanyCategory
from .permissions import IsCompanyUser
from .repository.company_repository import CompanyRepository
from .serializers import (
    OutputCompanySerializer,
    OutputCompanyListSerializer,
    OutputCompanyDetailsSerializer,
    InputCompanyEditSerializer,
    OutputCompanyCategorySerializer,
)
from .services.company import CompanyService


class CompanyCategoryListView(ListAPIView):
    queryset = CompanyCategory.objects.all()
    serializer_class = OutputCompanyCategorySerializer


class CompanyPublicListAPIView(APIView):
    _service = CompanyService(CompanyRepository())

    def get(self):
        companies = self._service.get_all_active()
        serializer = OutputCompanyListSerializer(companies, many=True)
        return Response(serializer.data)


class CompanyPublicRetrieveAPIView(APIView):
    _service = CompanyService(CompanyRepository())

    def get(self, slug: str):
        company = self._service.get_active_by_slug(slug)
        serializer = OutputCompanyDetailsSerializer(company)
        return Response(serializer.data)


class UserCompanyView(APIView):
    permission_classes = [IsAuthenticated]
    _service = CompanyService(CompanyRepository())

    def get(self, request):
        user = self.request.user
        company = self._service.get_company_by_user(user)
        serializer = OutputCompanySerializer(company)
        return Response(serializer.data)


class CompanyManagementApiView(APIView):
    permission_classes = [IsAuthenticated, IsCompanyUser]
    serializer_class = InputCompanyEditSerializer

    def put(self, request):
        # todo move logic to service layer
        company_id = request.data.get("company_id")
        company = get_object_or_404(Company, pk=company_id)
        serializer = self.serializer_class(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
