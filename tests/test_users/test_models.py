import pytest
from users.models import UserAccount


@pytest.mark.django_db
def test_create_user_success():
    user = UserAccount.objects.create(
        first_name="John",
        last_name="Doe",
        email="johndoe@example.com",
        password="XXXXXXXXXXX",
    )
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.email == "johndoe@example.com"
    assert user.is_active
    assert user.is_staff == False
    assert user.is_superuser == False
