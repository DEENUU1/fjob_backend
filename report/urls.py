from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSetUser,
    ReportViewSetAdmin,
    ReportViewListAdmin
)


router = DefaultRouter()
router.register("", ReportViewSetUser, basename="report_user")
router.register("dashboard", ReportViewSetAdmin, basename="report_admin")
router.register("dashboard/all", ReportViewListAdmin, basename="report_list")

urlpatterns = router.urls
