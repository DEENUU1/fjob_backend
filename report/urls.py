from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSetUser,
    ReportViewSetAdmin,
    ReportViewListAdmin
)
from django.urls import path


router = DefaultRouter()
router.register("", ReportViewSetUser, basename="report_user")
router.register("dashboard", ReportViewSetAdmin, basename="report_admin")


urlpatterns = [
    path("dashboard/all", ReportViewListAdmin.as_view(), name="report_list")
]

urlpatterns += router.urls
