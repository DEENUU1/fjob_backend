import pytest
from tests.fixtures import user, job_offer
from rest_framework.test import force_authenticate, APIRequestFactory
from candidate.views import SendApplicationView
import json
from candidate.models import Candidate

factory = APIRequestFactory()


def application_data(user, job_offer):
    return json.dumps({
        "full_name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "user": user.id,
        "offer": job_offer.id,
        "message": "This is a test message to the recruiter",
        "url": "https://example.com",
        "offer_id": job_offer.id,
    })


@pytest.mark.django_db
def test_send_application_success(user, job_offer):
    data = application_data(user, job_offer)
    view = SendApplicationView.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == 201
    assert response.data["full_name"] == "John Doe"
    assert response.data["email"] == "john@example.com"
    assert response.data["phone"] == "+1234567890"
    assert response.data["user"] == user.id
    assert response.data["offer"] == job_offer.id
    assert response.data["message"] == "This is a test message to the recruiter"
    assert response.data["url"] == "https://example.com"
    assert response.data["status"] == "Pending"


@pytest.mark.django_db
def test_send_application_unauthenticated(user, job_offer):
    data = application_data(user, job_offer)
    view = SendApplicationView.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_send_application_no_offer_id(user, job_offer):
    data = application_data(user, job_offer)
    data = json.loads(data)
    data.pop("offer_id")
    data = json.dumps(data)
    view = SendApplicationView.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == 400
    assert response.data["info"] == "Offer id is required"


@pytest.mark.django_db
def test_send_application_user_already_applied_for_job_offer(user, job_offer):
    Candidate.objects.create(user=user, offer=job_offer)

    data = application_data(user, job_offer)
    view = SendApplicationView.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == 400
    assert response.data["info"] == "You have already applied for this job offer"