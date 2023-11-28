from rest_framework.routers import DefaultRouter
from .views import (
    CompanyViewSet,
    UserCheckCompanyView,
)
from django.urls import path



router = DefaultRouter()
router.register("", CompanyViewSet, basename="company_basic")

urlpatterns = [
    path("check/", UserCheckCompanyView.as_view(), name="check_user_company"),
]

urlpatterns += router.urls

