from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from .models import Contact, Report


class ContactSerializer(ModelSerializer):
    is_new = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = "__all__"


class ReportSerializer(ModelSerializer):
    is_new = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = "__all__"
