from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CandidateCreateView,
    CandidateUserListView,
    CandidateCompanyViewSet,
    CandidateCompanyListView,
    CountCandidateStatus,
    NumCandidatePerDayTimeline,
    CandidateCreateAPIView
)

router = DefaultRouter()
router.register("candidate", CandidateCompanyViewSet, basename="candidate_management")

urlpatterns = [
    path("candidate/", CandidateCreateAPIView.as_view(), name="candidate_create"),
    path("candidate/offer/<int:job_offer_id>/", CandidateCompanyListView.as_view(), name="candidate_list_offer"),
    path("candidate/user/", CandidateUserListView.as_view(),  name="candidate_list_user"),
    path("candidate/<int:job_offer_id>/stat", CountCandidateStatus.as_view(), name="candidate_list_stat"),
    path("candidate/<int:job_offer_id>/timeline", NumCandidatePerDayTimeline.as_view(), name="candidate_list_timeline")
]

urlpatterns += router.urls
