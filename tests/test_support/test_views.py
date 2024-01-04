import json

import pytest
from rest_framework.test import force_authenticate, APIRequestFactory

from support.models import Contact, Report
from support.views import ContactCreateAPIView, ReportCreateAPIView
from tests.fixtures import user, job_offer

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_create_contact_object():
    request = factory.post(
        '/api/support/contact/',
        json.dumps({
            "subject": "test message",
            "message": "test message",
            "email": "test@example.com",
        }),
        content_type='application/json'
    )
    view = ContactCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 201
    assert Contact.objects.count() == 1


@pytest.mark.django_db
def test_success_create_report_object(user, job_offer):
    request = factory.post(
        '/api/support/report',
        json.dumps({
            "user": user.id,
            "offer": job_offer.id,
            "description": "test report",
        }),
        content_type='application/json'
    )
    force_authenticate(request, user=user)
    view = ReportCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 201
    assert Report.objects.count() == 1


@pytest.mark.django_db
def test_error_create_report_object_not_authenticated(user, job_offer):
    request = factory.post(
        '/api/support/report',
        json.dumps({
            "user": user.id,
            "offer": job_offer.id,
            "description": "test report",
        }),
        content_type='application/json'
    )

    view = ReportCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 401
    assert Report.objects.count() == 0
