from .models import Package
from rest_framework.serializers import ModelSerializer


class PackageSerializer(ModelSerializer):
    class Meta:
        model = Package
        fields = "__all__"
