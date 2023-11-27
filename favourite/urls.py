from .views import (
    FavouriteView,
)
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register('favourite', FavouriteView, basename='favourite')

urlpatterns = router.urls

