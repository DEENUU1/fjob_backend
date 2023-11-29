from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import status
from .models import (
    Favourite,
)
from .serializers import (
    FavouriteSerializer,
)
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404


class FavouriteView(ViewSet):
    permission_classes = [IsAuthenticated,]

    def list(self, request):
        favourites = Favourite.objects.filter(user=request.user)
        serializer = FavouriteSerializer(favourites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
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
