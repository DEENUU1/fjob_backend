from .views import (
    FavouriteView,
    FavouriteCountAPIView,
)
from rest_framework.routers import DefaultRouter
from django.urls import path


router = DefaultRouter()
router.register("", FavouriteView, basename="favourite")

urlpatterns = [
    path("counter/<int:offer_id>/", FavouriteCountAPIView.as_view(), name="favourite-count"),
]

urlpatterns += router.urls

