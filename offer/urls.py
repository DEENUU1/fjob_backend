from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    WorkTypeView,
    EmploymentTypeView,
    ExperienceView,
    SalaryView,
    OfferListView,
    JobOfferView,
    CompanyOfferListView,
    OfferViewSet,
    ScrapedDataView,
)

router = DefaultRouter()
router.register("work", WorkTypeView, basename="work_type")
router.register("employment", EmploymentTypeView, basename="employment_type")
router.register("experience", ExperienceView, basename="experience_type")
router.register("offer", JobOfferView, basename="job_offer")
router.register("company", OfferViewSet, basename="company_crud")

urlpatterns = [
    path("salary/", SalaryView.as_view(), name="salary_stats"),
    path("offer/", OfferListView.as_view(), name="offer_list"),
    path("offer/company/<str:slug>", CompanyOfferListView.as_view(), name="company_offer_list"),
    path("scrape/", ScrapedDataView.as_view(), name="save_scraped_data"),
]
urlpatterns += router.urls
