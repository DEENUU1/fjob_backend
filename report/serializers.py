from rest_framework.serializers import ModelSerializer
from .models import Report
from rest_framework import serializers


class ReportSerializer(ModelSerializer):
    is_new = serializers.ReadOnlyField()

    class Meta:
        model = Report
        fields = "__all__"
