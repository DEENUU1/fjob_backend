from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CandidateCreateView,
    CandidateUserListView,
    CandidateCompanyRetrieveUpdateViewSet,
    CandidateCompanyListView,
)

router = DefaultRouter()
router.register("candidate", CandidateCompanyRetrieveUpdateViewSet, basename="candidate_management")

urlpatterns = [
    path("candidate/", CandidateCreateView.as_view(), name="candidate_create"),
    path("candidate/offer/<int:job_offer_id>/", CandidateCompanyListView.as_view(), name="candidate_list_offer"),
    path("candidate/user/", CandidateUserListView.as_view(),  name="candidate_list_user"),
]

urlpatterns += router.urls
