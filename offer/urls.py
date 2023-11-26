from rest_framework.routers import DefaultRouter
from .views import WorkTypeView, EmploymentTypeView, ExperienceView

router = DefaultRouter()
router.register("work", WorkTypeView, basename="work_type")
router.register("employment", EmploymentTypeView, basename="employment_type")
router.register("experience", ExperienceView, basename="experience_type")

urlpatterns = router.urls
