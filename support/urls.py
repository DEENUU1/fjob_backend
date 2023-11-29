from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewUser,
)


router = DefaultRouter()
router.register("contact", ContactViewUser, basename="contact_post")
router.register("report", ReportCreateView, basename="report_user")

urlpatterns = router.urls
