from rest_framework.serializers import ModelSerializer
from .models import Statistics


class StatisticsSerializer(ModelSerializer):
    class Meta:
        model = Statistics
        fields = '__all__'
