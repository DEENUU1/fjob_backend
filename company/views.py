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
    """
    API view for listing all CompanyCategory objects.

    Attributes:
    - queryset: The queryset containing all CompanyCategory objects.
    - serializer_class: The serializer class for CompanyCategory objects.
    """

    queryset = CompanyCategory.objects.all()
    serializer_class = OutputCompanyCategorySerializer


class CompanyPublicListAPIView(APIView):
    """
    API view for listing all active companies publicly.

    Attributes:
    - _service: An instance of the CompanyService for handling company-related operations.
    """

    _service = CompanyService(CompanyRepository())

    def get(self):
        """
        Handles the HTTP GET request to retrieve a list of all active companies.

        Returns:
        - Response: The serialized data of active companies.
        """
        companies = self._service.get_all_active()
        serializer = OutputCompanyListSerializer(companies, many=True)
        return Response(serializer.data)


class CompanyPublicRetrieveAPIView(APIView):
    """
    API view for retrieving details of a specific active company publicly.

    Attributes:
    - _service: An instance of the CompanyService for handling company-related operations.
    """

    _service = CompanyService(CompanyRepository())

    def get(self, slug: str):
        """
        Handles the HTTP GET request to retrieve details of a specific active company.

        Parameters:
        - slug (str): The slug of the company.

        Returns:
        - Response: The serialized data of the company details.
        """
        company = self._service.get_active_by_slug(slug)
        serializer = OutputCompanyDetailsSerializer(company)
        return Response(serializer.data)


class UserCompanyView(APIView):
    """
    API view for retrieving details of the company associated with the authenticated user.

    Attributes:
    - permission_classes: The permissions required for accessing this view.
    - _service: An instance of the CompanyService for handling company-related operations.
    """

    permission_classes = (IsAuthenticated, )
    _service = CompanyService(CompanyRepository())

    def get(self, request):
        """
        Handles the HTTP GET request to retrieve details of the company associated with the authenticated user.

        Returns:
        - Response: The serialized data of the company details.
        """
        user = self.request.user
        company = self._service.get_company_by_user(user)
        serializer = OutputCompanySerializer(company)
        return Response(serializer.data)


class CompanyManagementApiView(APIView):
    """
    API view for managing company details.

    Attributes:
    - permission_classes: The permissions required for accessing this view.
    """

    permission_classes = (IsAuthenticated, IsCompanyUser, )

    def put(self, request):
        """
        Handles the HTTP PUT request to update company details.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The serialized data of the updated company details.
        """
        # todo move logic to service layer
        company_id = request.data.get("company_id")
        company = get_object_or_404(Company, pk=company_id)
        serializer = InputCompanyEditSerializer(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
