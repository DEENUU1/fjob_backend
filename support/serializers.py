from rest_framework.serializers import ModelSerializer

from .models import Contact, Report


class ContactSerializer(ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"


class ReportSerializer(ModelSerializer):
    class Meta:
        model = Report
        fields = "__all__"
