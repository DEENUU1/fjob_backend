from rest_framework.routers import DefaultRouter
from .views import WorkTypeView, EmploymentTypeView

router = DefaultRouter()
router.register("work", WorkTypeView, basename="work_type")
router.register("employment", EmploymentTypeView, basename="employment_type")


urlpatterns = router.urls