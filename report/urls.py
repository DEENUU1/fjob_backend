from rest_framework.routers import DefaultRouter
from .views import (
    ReportCreateView,
    ReportViewSetAdmin,
    ReportListViewAdmin
)
from django.urls import path


router = DefaultRouter()
router.register("", ReportCreateView, basename="report_user")
router.register("dashboard", ReportViewSetAdmin, basename="report_admin")


urlpatterns = [
    path("dashboard/all", ReportListViewAdmin.as_view(), name="report_list")
]

urlpatterns += router.urls
