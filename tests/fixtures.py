from users.models import UserAccount
import pytest
from offer.models import JobOffer


@pytest.fixture
def user():
    return UserAccount.objects.create_user(
        first_name="John",
        last_name="Doe",
        email="test@example.com",
        password="XXXXXXXXXXX",
    )


@pytest.fixture
def job_offer(user):
    return JobOffer.objects.create(
        title="Test Job Offer",
        description="Test Job Offer Description",
    )
