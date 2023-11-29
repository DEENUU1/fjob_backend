from rest_framework.routers import DefaultRouter
from .views import (
    ReportCreateView,
)


router = DefaultRouter()
router.register("", ReportCreateView, basename="report_user")


urlpatterns = router.urls
