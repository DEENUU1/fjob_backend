from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import status
from rest_framework.generics import ListAPIView
from django_filters import rest_framework as filters
from fjob.pagination import CustomPagination
from .models import (
    Contact
)
from .serializers import (
    ContactSerializer
)
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAdminUser


class ContactViewUser(ViewSet):

    def create(self, request):
        serializer = ContactSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
