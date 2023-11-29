from rest_framework.routers import DefaultRouter
from .views import (
    CompanyPublicView,
    CompanyUserView,
    UserHasCompanyView,
    CompanyOfferView,
    CompanyOfferListView,
    UserCanMakeCompanyView
)
from django.urls import path


router = DefaultRouter()
router.register("management", CompanyUserView, basename="company_user")
router.register("company", CompanyPublicView, basename="company_public")
router.register("offer", CompanyOfferView, basename="manage_company")
router.register("user/check/new", UserCanMakeCompanyView, basename="check_user_new_company")

urlpatterns = [
    path("user/check/company/", UserHasCompanyView.as_view(), name="check_user_company"),
    path("offer/all", CompanyOfferListView.as_view(), name="list_of_company_offers_private"),
]

urlpatterns += router.urls

