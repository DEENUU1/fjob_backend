from rest_framework.routers import DefaultRouter
from .views import (
    CompanyPublicView,
    CompanyUserView,
    UserCheckCompanyView,
)
from django.urls import path


router = DefaultRouter()
router.register("management", CompanyUserView, basename="company_user")
router.register("", CompanyPublicView, basename="company_public")

urlpatterns = [
    path("check/", UserCheckCompanyView.as_view(), name="check_user_company"),
]

urlpatterns += router.urls

