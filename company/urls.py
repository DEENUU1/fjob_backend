from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyPublicView,
    CompanyUserView,
    CompanyOfferView,
    CompanyOfferListView,
    UserCompanyView,
)

router = DefaultRouter()
# router.register("management", CompanyUserView, basename="company_user")
router.register("", CompanyPublicView, basename="company_public")
router.register("offer", CompanyOfferView, basename="manage_company")

urlpatterns = [
    path("offer/", CompanyOfferListView.as_view(), name="list_of_company_offers_private"),
    path("company/", UserCompanyView.as_view(), name="user_company_private"),
    path("management/", CompanyUserView.as_view(), name="user_company_management"),
]

urlpatterns += router.urls
