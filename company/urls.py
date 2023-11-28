from rest_framework.routers import DefaultRouter
from .views import (
    CompanyPublicView,
    CompanyUserView,
    UserCheckCompanyView,
    CompanyOfferView,
    CompanyOfferListView
)
from django.urls import path


router = DefaultRouter()
router.register("management", CompanyUserView, basename="company_user")
router.register("", CompanyPublicView, basename="company_public")
router.register("company", CompanyOfferView, basename="manage_company")

urlpatterns = [
    path("check/", UserCheckCompanyView.as_view(), name="check_user_company"),
    path("company/offer", CompanyOfferListView.as_view(), name="list_of_campany_offers"),
]

urlpatterns += router.urls

