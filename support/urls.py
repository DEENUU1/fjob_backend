from .views import (
    ContactCreateAPIView,
    ReportCreateAPIView
)

from django.urls import path


urlpatterns = [
    path("contact/",  ContactCreateAPIView.as_view(), name="create_contact_object"),
    path("report/", ReportCreateAPIView.as_view(), name="create_report_object"),
]
