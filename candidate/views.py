from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from offer.models import JobOffer


class SendApplicationView(ViewSet):
    def create(self, request):
        offer_id = request.data.get("offer_id")
        if offer_id is None:
            return Response({"info": "Wrong offer id"}, status=status.HTTP_400_BAD_REQUEST)

        offer = JobOffer.objects.filter(pk=offer_id)
        if not offer:
            return Response({"info": "Wrong offer id"}, status=status.HTTP_400_BAD_REQUEST)

        if offer.apply_form is not None:
            return Response({"info": "You can't apply for this offer"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = CandidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class UserApplicationsView(ViewSet):
    def list(self, request):
        candidate = Candidate.objects.filter(user=request.user)
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)
