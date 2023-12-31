from rest_framework.serializers import ModelSerializer

from .models import Contact, Report


class ContactCreateSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = ["id", "subject", "message", "email"]


class ReportCreateSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "user", "offer", "description"]
