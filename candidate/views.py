from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import Candidate
from .serializers import CandidateSerializer
from offer.models import JobOffer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView


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
    permission_classes = [IsAuthenticated]

    def list(self, request):
        candidate = Candidate.objects.filter(user=request.user)
        serializer = CandidateSerializer(candidate, many=True)
        return Response(serializer.data)


class CandidateListView(generics.ListAPIView):
    serializer_class = CandidateSerializer
    permission_classes = [IsAuthenticated]

    #     path('job-offers/<int:offer_id>/candidates/', CandidateListView.as_view(), name='candidate-list'),
    def get_queryset(self):
        offer_id = self.kwargs['offer_id']
        user = self.request.user

        if user.company.joboffer_set.filter(id=offer_id).exists():
            return Candidate.objects.filter(offer_id=offer_id)
        else:
            return Candidate.objects.none()


#     path('candidates/<int:candidate_id>/change-status/<str:new_status>/', ChangeCandidateStatus.as_view(), name='change-candidate-status'),
class ChangeCandidateStatus(APIView):
    def patch(self, request, candidate_id, new_status):
        try:
            candidate = Candidate.objects.get(pk=candidate_id)
        except Candidate.DoesNotExist:
            return Response({'error': 'Candidate not found'}, status=status.HTTP_404_NOT_FOUND)

        valid_statuses = [s[0] for s in Candidate.STATUS]
        if new_status not in valid_statuses:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)

        candidate.status = new_status
        candidate.save()

        serializer = CandidateSerializer(candidate)
        return Response(serializer.data)