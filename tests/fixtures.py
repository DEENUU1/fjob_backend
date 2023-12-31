import pytest

from company.models import Company
from offer.models import JobOffer
from users.models import UserAccount


@pytest.fixture
def user():
    return UserAccount.objects.create(
        first_name="John",
        last_name="Doe",
        email="test@example.com",
        password="XXXXXXXXXXX",
    )


@pytest.fixture
def user_second():
    return UserAccount.objects.create(
        first_name="Jane",
        last_name="Doe",
        email="test2@example.com",
        password="XXXXXXXXXXX",
    )


@pytest.fixture
def user_no_available_companies():
    return UserAccount.objects.create(
        first_name="John",
        last_name="Doe",
        email="test3@example.com",
        password="XXXXXXXXXXX",
        num_of_available_companies=0
    )


@pytest.fixture
def job_offer(user):
    return JobOffer.objects.create(
        title="Test Job Offer",
        description="Test Job Offer Description",
        status="ACTIVE"
    )


@pytest.fixture
def job_offer_draft(user):
    return JobOffer.objects.create(
        title="Test Draft",
        description="xyz",
        status="DRAFT"
    )

@pytest.fixture
def company(user):
    return Company.objects.create(
        name="Test Company",
        user=user
    )


@pytest.fixture
def job_offer_with_company(user, company):
    return JobOffer.objects.create(
        title="Test Job Offer",
        company=company
    )
