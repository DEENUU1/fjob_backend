from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    ContactSerializer,
    ReportSerializer
)
from rest_framework.permissions import IsAuthenticated


class ContactViewUser(ViewSet):

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ReportCreateView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def create(self, request):
        serializer = ReportSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)