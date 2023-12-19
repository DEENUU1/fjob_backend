from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from offer.models import JobOffer
from .models import Candidate
from .serializers import CandidateSerializer


class CandidateViewSet(ViewSet):
    permission_classes = [IsAuthenticated]

    def create(self, request):
        offer_id = request.data.get("offer_id")

        if offer_id is None:
            return Response({"info": "Offer id is required"}, status=status.HTTP_400_BAD_REQUEST)

        offer = JobOffer.objects.filter(pk=offer_id).first()
        if not offer:
            return Response({"info": "Wrong offer id"}, status=status.HTTP_400_BAD_REQUEST)

        candidate = Candidate.objects.filter(offer_id=offer_id, user=request.user).exists()
        if candidate:
            return Response({"info": "You have already applied for this job offer"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request):
        candidate = Candidate.objects.filter(user=request.user)
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)


class CandidateListView(APIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = self.request.user
        offer_id = self.kwargs.get("offer_id")

        if not offer_id:
            return Response({"info": "Offer id is required"}, status=status.HTTP_400_BAD_REQUEST)

        offer = JobOffer.objects.filter(pk=offer_id).first()
        if not offer:
            return Response({"info": "Job offer does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        if offer.company.user != user:
            return Response({"info": "You are not authorized to view this offer"}, status=status.HTTP_401_UNAUTHORIZED)

        candidates = Candidate.objects.filter(offer_id=offer_id).all()
        serializer = CandidateSerializer(candidates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeCandidateStatus(APIView):
    def patch(self, request, candidate_id, new_status):
        candidate = Candidate.objects.get(pk=candidate_id).first()

        if not candidate:
            return Response({"error": "Candidate not found"}, status=status.HTTP_404_NOT_FOUND)

        valid_statuses = [s[0] for s in Candidate.STATUS]
        if new_status not in valid_statuses:
            return Response({"error": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)

        candidate._previous_status = candidate.status

        candidate.status = new_status
        candidate.save()

        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)
