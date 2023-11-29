from rest_framework.routers import DefaultRouter
from .views import (
    CompanyPublicView,
    CompanyUserView,
    UserCheckHasCompanyView,
    CompanyOfferView,
    CompanyOfferListView
)
from django.urls import path


router = DefaultRouter()
router.register("management", CompanyUserView, basename="company_user")
router.register("company", CompanyPublicView, basename="company_public")
router.register("offer", CompanyOfferView, basename="manage_company")

urlpatterns = [
    path("check/", UserCheckHasCompanyView.as_view(), name="check_user_company"),
    path("company/offer", CompanyOfferListView.as_view(), name="list_of_campany_offers"),
]

urlpatterns += router.urls

