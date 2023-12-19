from rest_framework.routers import DefaultRouter
from .views import (
    CompanyPublicView,
    CompanyUserView,
    # UserHasCompanyView,
    CompanyOfferView,
    CompanyOfferListView,
    # UserCanMakeCompanyView
)
from django.urls import path


router = DefaultRouter()
router.register("management", CompanyUserView, basename="company_user")
router.register("", CompanyPublicView, basename="company_public")
router.register("offer", CompanyOfferView, basename="manage_company")


urlpatterns = [
    # path("user/check/company/", UserHasCompanyView.as_view(), name="check_user_company"),
    # path("user/check/new", UserCanMakeCompanyView.as_view(), name="check_user_can_make_new_company"),
    path("offer/", CompanyOfferListView.as_view(), name="list_of_company_offers_private"),
]

urlpatterns += router.urls

