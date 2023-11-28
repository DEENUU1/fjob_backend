from rest_framework.viewsets import ViewSet
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
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


class ReportCreateView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportListViewAdmin(ListAPIView):
    permission_classes = [IsAdminUser, ]
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)

    # Report fields by which objects can be ordered
    ordering_fields = [
        'created_at',
    ]
    # Report fields by which objects can be searched
    # @ allows to run Full-text search - support only for PostgreSQL
    # $ regex
    # ^ starts with
    # = exact matches
    search_fields = ["^description"]

    # Report fields by which objects can be filtered
    filterset_fields = [
        "reviewed"
    ]

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ReportViewSetAdmin(ViewSet):
    permission_classes = [IsAdminUser, ]

    def retrieve(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        serializer = ReportSerializer(report)
        return Response(serializer.data)

    def update(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        current_reviewed_value = report.reviewed

        report.reviewed = not current_reviewed_value
        report.save()

        serializer = ReportSerializer(report)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        report = get_object_or_404(Report, pk=pk)
        report.delete()
