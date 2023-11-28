from rest_framework.serializers import ModelSerializer
from .models import Contact
from rest_framework import serializers


class ContactSerializer(ModelSerializer):
    is_new = serializers.ReadOnlyField()
    is_expired = serializers.ReadOnlyField()

    class Meta:
        model = Contact
        fields = "__all__"
