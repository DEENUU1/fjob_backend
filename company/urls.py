from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
)


router = DefaultRouter()
router.register("", CompanyViewSet, basename="company")


urlpatterns = router.urls

