from django.urls import path

from .views import (
    CompanyPublicListAPIView,
    CompanyPublicRetrieveAPIView,
    CompanyManagementApiView,
    UserCompanyView,
    CompanyCategoryListView,
)


urlpatterns = [
    path(
        "<str:slug>",
        CompanyPublicRetrieveAPIView.as_view(),
        name="company_public_retrieve"
    ),
    path(
        "",
        CompanyPublicListAPIView.as_view(),
        name="company_public_list"
    ),
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

