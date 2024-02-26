import pytest

from candidates.models import Candidate
from offer.models import JobOffer
from users.models import UserAccount


@pytest.fixture
def job_offer_instance():
    return JobOffer.objects.create(
        title="Test Job Offer",
        description="Test Job Offer Description",
        is_remote=True,
        is_hybrid=False,
        skills="Test Skills",
        company_logo="test_logo.png",
        company_name="Test Company",
        url="http://testjoboffer.com"
    )


@pytest.fixture
def user_account_instance():
    return UserAccount.objects.create(
        first_name="testuser",
        last_name="xxx",
        email="testuser@example.com",
        password="testpassword"
    )


@pytest.fixture
def candidate_instance(job_offer_instance, user_account_instance):
    return Candidate.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="123456789",
        future_recruitment=False,
        message="Test Message",
        job_offer=job_offer_instance,
        user=user_account_instance,
        status="PENDING",
    )


@pytest.mark.django_db
def test_candidate_model(candidate_instance, job_offer_instance, user_account_instance):
    assert candidate_instance.first_name == "John"
    assert candidate_instance.last_name == "Doe"
    assert candidate_instance.email == "john.doe@example.com"
    assert candidate_instance.phone == "123456789"
    assert candidate_instance.future_recruitment is False
    assert candidate_instance.message == "Test Message"
    assert candidate_instance.job_offer == job_offer_instance
    assert candidate_instance.user == user_account_instance
    assert candidate_instance.status == "PENDING"


@pytest.mark.django_db
def test_candidate_model_blank_fields(job_offer_instance):
    candidate = Candidate.objects.create(
        first_name="John",
        last_name="Doe",
        email="john.doe@example.com",
        phone="123456789",
        job_offer=job_offer_instance
    )
    assert candidate.message is None
    assert candidate.user is None
