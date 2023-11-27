from .views import (
    FavouriteView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("", FavouriteView, basename="favourite")

urlpatterns = router.urls

