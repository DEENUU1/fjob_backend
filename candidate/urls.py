from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import (
    CandidateViewSet,
    CandidateListView,
    ChangeCandidateStatus
)

router = DefaultRouter()
router.register("", CandidateViewSet, basename="send_application")

urlpatterns = [
    path("<int:offer_id>/", CandidateListView.as_view(), name="list_of_candidates_for_specified_offer"),
    path("status/<int:candidate_id>/", ChangeCandidateStatus.as_view(), name="change_candidate_status"),

]

urlpatterns += router.urls
