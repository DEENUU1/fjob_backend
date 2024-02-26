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
    """
    API view for handling Favourite operations.

    Attributes:
    - permission_classes: The permissions required for accessing this view.
    - _service: An instance of the FavouriteService for handling favourite-related operations.
    """

    permission_classes = (IsAuthenticated,)
    _service = FavouriteService(FavouriteRepository())

    def get(self, request):
        """
        Handles the HTTP GET request to retrieve all favourites for the authenticated user.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The serialized data of all favourites.
        """
        favourites = self._service.get_all(request.user)
        serializer = OutputFavouriteSerializerList(favourites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        """
        Handles the HTTP POST request to create a new favourite.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The serialized data of the created favourite.
        """
        serializer = InputFavouriteSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self._service.create(serializer.validated_data)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, pk):
        """
        Handles the HTTP DELETE request to delete a favourite.

        Parameters:
        - request: The HTTP request object.
        - pk: The primary key of the favourite to be deleted.

        Returns:
        - Response: An empty response indicating successful deletion.
        """
        self._service.delete(request.user, pk)
        return Response(status=status.HTTP_204_NO_CONTENT)
