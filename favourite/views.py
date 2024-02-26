from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .repository.favourite_repository import FavouriteRepository
from .serializers import (
    InputFavouriteSerializer,
    OutputFavouriteSerializerList

)
from .services.favourite import FavouriteService


class FavouriteAPIView(APIView):
    permission_classes = [IsAuthenticated, ]
    _service = FavouriteService(FavouriteRepository())

    def get(self, request):
        favourites = self._service.get_all(request.user)
        serializer = OutputFavouriteSerializerList(favourites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = InputFavouriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        self._service.delete(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
