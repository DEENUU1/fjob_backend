from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from .models import Company
from .permissions import IsCompanyUser
from .serializers import (
    CompanySerializer,
    CompanyListSerializer,
    CompanyDetailsSerializer,
    CompanyEditSerializer,
)



class CompanyPublicListRetrieveView(ViewSet):
    # Return a list and details of active Company models
    lookup_field = 'slug'
    queryset = Company.objects.filter(is_active=True)

    def list(self, request):
        serializer = CompanyListSerializer(self.queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, slug=None):
        company = get_object_or_404(self.queryset, slug=slug)
        serializer = CompanyDetailsSerializer(company)
        return Response(serializer.data)


class UserCompanyView(APIView):
    # Return Company object for the specified user object
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = self.request.user
        company = Company.objects.filter(user=user).first()
        if not company:
            return Response({"detail": "Company not found for the user"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CompanySerializer(company)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CompanyManagementApiView(APIView):
    # Allow user to edit or delete Company
    permission_classes = [IsAuthenticated, IsCompanyUser]
    serializer_class = CompanyEditSerializer

    def put(self, request):
        company_id = request.data.get("company_id")
        company = get_object_or_404(Company, pk=company_id)
        serializer = self.serializer_class(company, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

