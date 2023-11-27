from rest_framework.routers import DefaultRouter
from .views import (
    ContactViewUser,
    ContactListViewAdmin,
    ContactViewAdmin,

)
from django.urls import path


router = DefaultRouter()
router.register("contact", ContactViewUser, basename="contact_post")
router.register("dashboard", ContactViewAdmin, basename="contact_post")

urlpatterns = [
    path("dashboard/all", ContactListViewAdmin.as_view(), name="salary_stats"),
]

urlpatterns += router.urls
