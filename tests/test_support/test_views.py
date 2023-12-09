import pytest
from tests.fixtures import user, job_offer, job_offer_with_company, user_second, company
from rest_framework.test import force_authenticate, APIRequestFactory
from support.views import ContactViewUser, ReportCreateView
import json
from support.models import Contact, Report

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_create_contact_object():
    request = factory.post(
        '/api/support/',
        json.dumps({
            "subject": "test message",
            "message": "test message",
            "email": "test@example.com",
        }),
        content_type='application/json'
    )
    view = ContactViewUser.as_view({"post": "create"})
    response = view(request)

    assert response.status_code == 201
    assert Contact.objects.count() == 1