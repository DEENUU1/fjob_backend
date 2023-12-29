from rest_framework.routers import DefaultRouter

from .views import (
    FavouriteView,
)

router = DefaultRouter()
router.register("", FavouriteView, basename="favourite")

urlpatterns = router.urls
