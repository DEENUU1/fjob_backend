import pytest

from company.models import Company
from users.models import UserAccount


@pytest.fixture
def user_data():
    return UserAccount.objects.create(
        first_name="John",
        last_name="Doe",
        email="john@example.com",
        password="XXXXXXXX"
    )


@pytest.mark.django_db
def test_create_company_str(user_data):
    company = Company.objects.create(
        name="Test company",
        user=user_data
    )
    assert str(company) == "Test company"
    assert company.name == "Test company"
    assert company.id == 1
