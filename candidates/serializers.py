from rest_framework.serializers import ModelSerializer

from .models import Candidate


class CandidateCreateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = "__all__"


class CandidateUserSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "created_at",
            "job_offer",
            "user",
            "status",
        ]


class CandidateCompanyListSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "phone",
            "message",
            "created_at",
            "updated_at",
            "job_offer",
            "status",
            "cv"
        ]


class CandidateCompanyUpdateSerializer(ModelSerializer):
    class Meta:
        model = Candidate
        fields = [
            "id",
            "status"
        ]
