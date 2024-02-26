from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyPublicListAPIView,
    CompanyPublicRetrieveAPIView,
    CompanyManagementApiView,
    UserCompanyView,
    CompanyCategoryListView,
)

router = DefaultRouter()
router.register(
    "",
    CompanyPublicListAPIView,
    basename="company_public_list"
)

router.register(
    "<slug:slug>",
    CompanyPublicRetrieveAPIView,
    basename="company_public_retrieve"
)

urlpatterns = [
    path(
        "company/",
        UserCompanyView.as_view(),
        name="user_company_private"
    ),
    path(
        "management/",
        CompanyManagementApiView.as_view(),
        name="company_management"
    ),
    path(
        "category/",
        CompanyCategoryListView.as_view(),
        name="company_category_list"
    ),
]

urlpatterns += router.urls
