from rest_framework.serializers import ModelSerializer
from .models import Candidate, OfferCandidate


class CandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = '__all__'


class OfferCandidateSerializer(ModelSerializer):
    class Meta:
        model = OfferCandidate
        fields = '__all__'
