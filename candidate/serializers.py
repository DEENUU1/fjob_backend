from rest_framework.serializers import ModelSerializer
from .models import Candidate


class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'
