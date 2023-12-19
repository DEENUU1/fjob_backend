import pytest

from favourite.models import Favourite
from offer.models import JobOffer
from tests.test_company.test_models import user_data


@pytest.fixture
def offer_data(user_data):
    return JobOffer.objects.create(
        title="test",

    )


@pytest.mark.django_db
def test_create_favourite_object_success(user_data, offer_data):
    favourite = Favourite.objects.create(user=user_data, offer=offer_data)
    assert favourite.user == user_data
    assert favourite.offer.id == 1
    assert favourite.offer.title == "test"
