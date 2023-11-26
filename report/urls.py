from rest_framework.routers import DefaultRouter
from .views import (
    ReportViewSetUser
)
from django.urls import path


router = DefaultRouter()
router.register("report", ReportViewSetUser, basename="report_user")


urlpatterns = [
    # path("salary/", SalaryView.as_view(), name="salary_stats"),
    # path("offer/", OfferListView.as_view(), name="offer_list"),
]
urlpatterns += router.urls
