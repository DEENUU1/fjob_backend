from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSetUser,
    ReportViewSetAdmin,

)


router = DefaultRouter()
router.register("", ReportViewSetUser, basename="report_user")
router.register("dashboard", ReportViewSetAdmin, basename="report_admin")


urlpatterns = router.urls
