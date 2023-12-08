import pytest
from tests.fixtures import user, job_offer, job_offer_with_company, user_second, company
from rest_framework.test import force_authenticate, APIRequestFactory
from candidate.views import CandidateViewSet, CandidateListView
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
def test_success_send_application_create_candidate_object(user, job_offer):
    data = application_data(user, job_offer)
    view = CandidateViewSet.as_view({"post": "create"})
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
def test_error_send_application_return_unauthenticated_info(user, job_offer):
    data = application_data(user, job_offer)
    view = CandidateViewSet.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_error_send_application_return_wrong_offer_id(user, job_offer):
    data = application_data(user, job_offer)
    data = json.loads(data)
    data.pop("offer_id")
    data = json.dumps(data)
    view = CandidateViewSet.as_view({"post": "create"})
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
def test_success_send_application_user_already_applied_for_job_offer(user, job_offer):
    Candidate.objects.create(user=user, offer=job_offer)

    data = application_data(user, job_offer)
    view = CandidateViewSet.as_view({"post": "create"})
    request = factory.post(
        "/api/candidate/",
        data,
        content_type="application/json",
    )
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == 400
    assert response.data["info"] == "You have already applied for this job offer"


@pytest.mark.django_db
def test_success_user_application_list_view_return_list_of_sent_applications(user, job_offer):
    Candidate.objects.create(user=user, offer=job_offer)

    view = CandidateViewSet.as_view({"get": "list"})
    request = factory.get("/api/candidate/")
    force_authenticate(request, user)
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_error_user_aplication_list_view_return_unauthenticated_info(user, job_offer):
    view = CandidateViewSet.as_view({"get": "list"})
    request = factory.get("/api/candidate/")
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_success_return_list_of_candidates(user, job_offer_with_company):
    offer = job_offer_with_company
    view = CandidateListView.as_view()
    request = factory.get(f"/api/candidate/1")
    force_authenticate(request, user)
    response = view(request, offer_id=1)

    assert response.status_code == 200


@pytest.mark.django_db
def test_error_return_list_of_candidates_unauthenticated_info(user, job_offer_with_company):
    view = CandidateListView.as_view()
    request = factory.get(f"/api/candidate/1")
    response = view(request, offer_id=1)

    assert response.status_code == 401


@pytest.mark.django_db
def test_error_return_list_of_candidates_unauthorized_user(user_second, job_offer_with_company):
    view = CandidateListView.as_view()
    request = factory.get(f"/api/candidate/1")
    force_authenticate(request, user_second)
    response = view(request, offer_id=1)

    assert response.status_code == 401
