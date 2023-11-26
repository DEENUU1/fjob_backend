from rest_framework.routers import DefaultRouter
from .views import WorkTypeView, EmploymentTypeView, ExperienceView, SalaryView
from django.urls import path


router = DefaultRouter()
router.register("work", WorkTypeView, basename="work_type")
router.register("employment", EmploymentTypeView, basename="employment_type")
router.register("experience", ExperienceView, basename="experience_type")


urlpatterns = [
    path("salary/", SalaryView.as_view(), name="salary_stats"),

]
urlpatterns += router.urls