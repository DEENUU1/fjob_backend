from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewUser,
)


router = DefaultRouter()
router.register("", ContactViewUser, basename="contact_post")

urlpatterns = router.urls
