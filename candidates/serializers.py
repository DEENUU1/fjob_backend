from rest_framework.serializers import ModelSerializer

from .models import Candidate
from offer.serializers import JobOfferHelperSerializer


class InputCandidateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"


class OutputCandidateUserSerializer(ModelSerializer):
    job_offer = JobOfferHelperSerializer()

    class Meta:
        model = Candidate
        fields = [
            "id",
            "created_at",
            "job_offer",
            "user",
            "status",
        ]


class OutputCandidateCompanyListSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "future_recruitment",
            "message",
            "created_at",
            "updated_at",
            "job_offer",
            "status",
            "cv"
        ]


class InputCandidateCompanyUpdateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "status"
        ]
