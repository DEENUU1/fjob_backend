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
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ContactListViewAdmin(ListAPIView):
    permission_classes = [IsAdminUser, ]
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer
    pagination_class = CustomPagination
    filter_backends = (filters.DjangoFilterBackend, OrderingFilter, SearchFilter)

    # Contact fields by which objects can be ordered
    ordering_fields = [
        "created_at",
    ]
    # Contact fields by which objects can be searched
    # @ allows to run Full-text search
    search_fields = ["@subject", "@message"]

    # Contact fields by which objects can be filtered
    filterset_fields = [
        "reviewed",
    ]

    def get(self, *args, **kwargs):
        return super().get(*args, **kwargs)


class ContactViewAdmin(ViewSet):
    permission_classes = [IsAdminUser, ]

    def retrieve(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        serializer = ContactSerializer(contact)
        return Response(serializer.data)

    def update(self, request, pk=None):
        contact = get_object_or_404(Contact, pk=pk)
        current_reviewed_value = contact.reviewed

        contact.reviewed = not current_reviewed_value
        contact.save()

        serializer = ContactSerializer(contact)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        report = get_object_or_404(Contact, pk=pk)
        report.delete()
