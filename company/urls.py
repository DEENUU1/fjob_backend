from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CompanyPublicListRetrieveView,
    CompanyManagementApiView,
    UserCompanyView,
)

router = DefaultRouter()
router.register("", CompanyPublicListRetrieveView, basename="company_public")

urlpatterns = [
    path("company/", UserCompanyView.as_view(), name="user_company_private"),
    path("management/", CompanyManagementApiView.as_view(), name="company_management"),
]

urlpatterns += router.urls
