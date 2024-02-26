from rest_framework.serializers import ModelSerializer

from .models import Contact, Report


class InputContactCreateSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "subject", "message", "email"]


class InputReportCreateSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "user", "offer", "description"]
