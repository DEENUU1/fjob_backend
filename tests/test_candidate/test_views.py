import json

import pytest
from rest_framework.test import force_authenticate, APIRequestFactory

from candidates.models import Candidate
from candidates.views import CandidateCreateAPIView, CandidateUserListView, CountCandidateStatus
from company.models import Company
from offer.models import JobOffer
from users.models import UserAccount

factory = APIRequestFactory()


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name="test", last_name="test", email="test@example.com")


@pytest.fixture
def another_user():
    return UserAccount.objects.create(first_name="test", last_name="test", email="tes2t@example.com")


@pytest.mark.django_db
def test_candidate_create_api_view_success():
    JobOffer.objects.create(title="test")

    request = factory.post(
        'api/candidate/candidate/',
        json.dumps({
            "first_name": "test",
            "last_name": "test",
            "email": "test@example.com",
            "phone": "123123123",
            "job_offer": 1
        }),
        content_type="application/json"
    )
    view = CandidateCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 201
    assert Candidate.objects.count() == 1


@pytest.mark.django_db
def test_candidate_create_api_view_error_invalid_job_offer_id():
    request = factory.post(
        'api/candidate/candidate/',
        json.dumps({
            "first_name": "test",
            "last_name": "test",
            "email": "test@example.com",
            "phone": "123123123",
            "job_offer": 1
        }),
        content_type="application/json"
    )
    view = CandidateCreateAPIView.as_view()
    response = view(request)

    assert response.status_code == 400
    assert Candidate.objects.count() == 0


@pytest.mark.django_db
def test_candidate_user_list_view_success(user):
    request = factory.get(
        "api/candidate/candidate/user"
    )
    force_authenticate(request, user=user)
    view = CandidateUserListView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data == []


@pytest.mark.django_db
def test_candidate_user_list_view_error_unauthorized_user():
    request = factory.get(
        "api/candidate/candidate/user"
    )
    view = CandidateUserListView.as_view()
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_count_candidate_status_success(user):
    company = Company.objects.create(name="test", user=user)
    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/stat"
    )
    force_authenticate(request, user=user)
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 200


@pytest.mark.django_db
def test_count_candidate_status_error_forbidden(user, another_user):
    company = Company.objects.create(name="test", user=another_user)

    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/stat"
    )
    force_authenticate(request, user=user)
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 403


@pytest.mark.django_db
def test_count_candidate_status_error_unauthorized(user, another_user):
    company = Company.objects.create(name="test", user=another_user)

    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/stat"
    )
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 401


@pytest.mark.django_db
def test_num_candidate_per_day_timeline_success(user):
    company = Company.objects.create(name="test", user=user)

    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/timeline"
    )
    force_authenticate(request, user=user)
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 200


@pytest.mark.django_db
def test_num_candidate_per_day_timeline_error_forbidden(user, another_user):
    company = Company.objects.create(name="test", user=another_user)

    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/timeline"
    )
    force_authenticate(request, user=user)
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 403


@pytest.mark.django_db
def test_num_candidate_per_day_timeline_error_unauthorized(user):
    company = Company.objects.create(name="test", user=user)

    job_offer = JobOffer.objects.create(title="test", company=company)
    Candidate.objects.create(first_name="test", last_name="test", email="test@example.com", job_offer=job_offer)

    request = factory.get(
        "api/candidate/candidate/1/timeline"
    )
    view = CountCandidateStatus.as_view()
    response = view(request, 1)

    assert response.status_code == 401
