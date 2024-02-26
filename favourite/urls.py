from django.urls import path
from .views import (
    FavouriteAPIView,
)


urlpatterns = [
    path("", FavouriteAPIView.as_view(), name="favourite_list_create_delete"),

]
