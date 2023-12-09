from rest_framework.routers import DefaultRouter
from .views import (
    WorkTypeView,
    EmploymentTypeView,
    ExperienceView,
    SalaryView,
    OfferListView,
    JobOfferView,
    CompanyOfferListView,

)
from django.urls import path


router = DefaultRouter()
router.register("work/", WorkTypeView, basename="work_type")
router.register("employment/", EmploymentTypeView, basename="employment_type")
router.register("experience/", ExperienceView, basename="experience_type")
router.register("offer/", JobOfferView, basename="job_offer")


urlpatterns = [
    path("salary/", SalaryView.as_view(), name="salary_stats"),
    path("offer/", OfferListView.as_view(), name="offer_list"),
    path("offer/company/<int:company_id>", CompanyOfferListView.as_view(), name="company_offer_list"),
]
urlpatterns += router.urls
