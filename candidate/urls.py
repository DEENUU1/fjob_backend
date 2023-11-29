from rest_framework.routers import DefaultRouter
from .views import (
    SendApplicationView,
    UserApplicationsView,
    CandidateListView,
    ChangeCandidateStatus
)
from django.urls import path


router = DefaultRouter()
router.register("", SendApplicationView, basename="send_application")
router.register("user/application", UserApplicationsView, basename="list_of_application_for_user")


urlpatterns = [
    path("candidate/<int:offer_id>/", CandidateListView.as_view(), name="list_of_candidates_for_specified_offer"),
    path("candidate/<int:candidate_id>/", ChangeCandidateStatus.as_view(), name="change_candidate_status"),

]

urlpatterns += router.urls
