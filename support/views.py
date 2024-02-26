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
    """
    API view for creating a new Contact.

    Attributes:
    - _service: An instance of the ContactService for handling contact-related operations.
    """

    _service = ContactService(ContactRepository())

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to create a new Contact.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The serialized data of the created Contact.
        """
        serializer = InputContactCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportCreateAPIView(APIView):
    """
    API view for creating a new Report.

    Attributes:
    - permission_classes: The permissions required for accessing this view.
    - _service: An instance of the ReportService for handling report-related operations.
    """

    permission_classes = (IsAuthenticated, )
    _service = ReportService(ReportRepository())

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to create a new Report.

        Parameters:
        - request: The HTTP request object.
        - args: Additional arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        - Response: The serialized data of the created Report.
        """
        serializer = InputReportCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
