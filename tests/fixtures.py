from users.models import UserAccount
import pytest
from offer.models import JobOffer
from company.models import Company


@pytest.fixture
def user():
    return UserAccount.objects.create_user(
        first_name="John",
        last_name="Doe",
        email="test@example.com",
        password="XXXXXXXXXXX",
    )

@pytest.fixture
def user_second():
    return UserAccount.objects.create_user(
        first_name="Jane",
        last_name="Doe",
        email="test2@example.com",
        password="XXXXXXXXXXX",
    )


@pytest.fixture
def job_offer(user):
    return JobOffer.objects.create(
        title="Test Job Offer",
        description="Test Job Offer Description",
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