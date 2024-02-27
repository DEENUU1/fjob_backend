from django.urls import path
from .views import (
    FavouriteListCreateAPIView,
    FavouriteDeleteAPIView
)


urlpatterns = [
    path("", FavouriteListCreateAPIView.as_view(), name="favourite_list_create_delete"),
    path("<int:pk>/", FavouriteDeleteAPIView.as_view(), name="favourite_delete_by_id")
]
