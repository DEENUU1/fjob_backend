import pytest
from rest_framework.exceptions import NotFound

from favourite.repository.favourite_repository import FavouriteRepository
from offer.models import JobOffer
from users.models import UserAccount


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name="test", last_name="user", email="test@example.com")


@pytest.fixture
def job_offer():
    return JobOffer.objects.create(title="Software Engineer")


@pytest.fixture
def repository():
    return FavouriteRepository()


@pytest.mark.django_db
def test_create_favourite(repository, user, job_offer):
    favourite_data = {
        "user": user,
        "offer": job_offer,
    }
    favourite = repository.create(favourite_data)
    assert favourite.id is not None
    assert favourite.user == user
    assert favourite.offer == job_offer


@pytest.mark.django_db
def test_get_all_favourites(repository, user, job_offer):
    favourites = repository.get_all()
    assert len(favourites) == 0

    favourite_data = {
        "user": user,
        "offer": job_offer,
    }
    repository.create(favourite_data)

    favourites = repository.get_all()
    assert len(favourites) == 1
    assert favourites[0].user == user
    assert favourites[0].offer == job_offer


@pytest.mark.django_db
def test_get_favourite_by_id(repository, user, job_offer):
    favourite_data = {
        "user": user,
        "offer": job_offer,
    }
    created_favourite = repository.create(favourite_data)

    retrieved_favourite = repository.get_by_id(created_favourite.id)
    assert retrieved_favourite is not None
    assert retrieved_favourite.user == user
    assert retrieved_favourite.offer == job_offer


@pytest.mark.django_db
def test_update_favourite(repository, user, job_offer):
    favourite_data = {
        "user": user,
        "offer": job_offer,
    }
    created_favourite = repository.create(favourite_data)

    updated_data = {"user": user, "offer": job_offer}
    updated_favourite = repository.update(created_favourite.id, updated_data)

    assert updated_favourite is not None
    assert updated_favourite.user == user
    assert updated_favourite.offer == job_offer


@pytest.mark.django_db
def test_delete_favourite(repository, user, job_offer):
    favourite_data = {
        "user": user,
        "offer": job_offer,
    }
    created_favourite = repository.create(favourite_data)

    repository.delete(created_favourite.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_favourite.id)
