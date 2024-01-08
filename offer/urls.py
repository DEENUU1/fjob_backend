from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    WorkTypeListAPIView,
    EmploymentTypeListAPIView,
    ExperienceListAPIView,
    SalaryView,
    OfferListView,
    JobOfferRetrieveAPIView,
    CompanyPublicOfferListView,
    OfferPrivateCompanyViewSet,
    ScrapedDataView,
    JobOfferRateCreateAPIView,
)

router = DefaultRouter()
router.register("company", OfferPrivateCompanyViewSet, basename="company_crud")

urlpatterns = [
    path("salary/", SalaryView.as_view(), name="salary_stats"),
    path("offer/", OfferListView.as_view(), name="offer_list"),
    path("offer/company/<str:slug>/", CompanyPublicOfferListView.as_view(), name="company_offer_list"),
    path("scrape/", ScrapedDataView.as_view(), name="save_scraped_data"),
    path("employment/", EmploymentTypeListAPIView.as_view(),  name="employment_type_list"),
    path("work/", WorkTypeListAPIView.as_view(), name="work_type_list"),
    path("experience/", ExperienceListAPIView.as_view(), name="experience_type_list"),
    path("offer/<str:slug>/", JobOfferRetrieveAPIView.as_view(), name="job_offer_detail"),
    path("offer/<str:slug>/rate", JobOfferRateCreateAPIView.as_view(), name="job_offer_rate_create"),
]
urlpatterns += router.urls
