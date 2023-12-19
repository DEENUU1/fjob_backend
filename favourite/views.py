from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet

from .models import (
    Favourite,
)
from .serializers import (
    FavouriteSerializer,
    FavouriteSerializerList

)


class FavouriteCountAPIView(APIView):
    def get(self, request, offer_id):
        try:
            favourite_count = Favourite.objects.filter(offer__id=offer_id).count()
            return Response({"counter": favourite_count}, status=status.HTTP_200_OK)
        except Exception:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class FavouriteView(ViewSet):
    permission_classes = [IsAuthenticated, ]

    def list(self, request):
        favourites = Favourite.objects.filter(user=request.user)
        serializer = FavouriteSerializerList(favourites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        offer_id = request.data.get('offer')
        existing_favourite = Favourite.objects.filter(
            user=request.user,
            offer=offer_id,
        ).first()

        if existing_favourite:
            return Response({"info": "Job Offer is already saved to Favourite"},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = FavouriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk):
        favourite = get_object_or_404(Favourite, pk=pk)
        if favourite.user != request.user:
            return Response(status=status.HTTP_403_FORBIDDEN)

        favourite.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
