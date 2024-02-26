from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import (
    InputContactCreateSerializer,
    InputReportCreateSerializer
)
from rest_framework.views import APIView
from support.services.contact import ContactService
from support.services.report import ReportService
from support.repository.contact_repository import ContactRepository
from support.repository.report_repository import ReportRepository


class ContactCreateAPIView(APIView):
    _service = ContactService(ContactRepository())

    def post(self, request, *args, **kwargs):
        serializer = InputContactCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    _service = ReportService(ReportRepository())

    def post(self, request, *args, **kwargs):
        serializer = InputReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
