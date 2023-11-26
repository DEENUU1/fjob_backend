from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from fjob.pagination import CustomPagination
from fjob.pagination import CustomPagination
from rest_framework.filters import OrderingFilter, SearchFilter
from django.shortcuts import get_object_or_404
from django_filters import rest_framework as filters
from .models import (
    Report
)
from .serializers import (
    ReportSerializer,
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser


class ReportViewSetUser(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
