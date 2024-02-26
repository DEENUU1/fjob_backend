import pytest
from rest_framework.exceptions import NotFound

from offer.models import JobOffer
from offer.repository.offer_rate_repository import JobOfferRateRepository
from users.models import UserAccount


@pytest.fixture
def repository():
    return JobOfferRateRepository()


@pytest.fixture
def job_offer():
    return JobOffer.objects.create(title="Software Engineer")


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name="test", last_name="user", email="test@example.com")


@pytest.mark.django_db
def test_create_job_offer_rate(repository, job_offer, user):
    job_offer_rate_data = {
        "job_offer": job_offer,
        "rate": 4,
    }
    job_offer_rate = repository.create(job_offer_rate_data)
    assert job_offer_rate.id is not None
    assert job_offer_rate.job_offer == job_offer
    assert job_offer_rate.rate == 4


@pytest.mark.django_db
def test_get_all_job_offer_rates(repository, job_offer, user):
    job_offer_rates = repository.get_all()
    assert len(job_offer_rates) == 0

    job_offer_rate_data = {
        "job_offer": job_offer,
        "rate": 5,
    }
    repository.create(job_offer_rate_data)

    job_offer_rates = repository.get_all()
    assert len(job_offer_rates) == 1
    assert job_offer_rates[0].rate == 5


@pytest.mark.django_db
def test_get_job_offer_rate_by_id(repository, job_offer, user):
    job_offer_rate_data = {
        "job_offer": job_offer,
        "rate": 3,
    }
    created_job_offer_rate = repository.create(job_offer_rate_data)

    retrieved_job_offer_rate = repository.get_by_id(created_job_offer_rate.id)
    assert retrieved_job_offer_rate is not None
    assert retrieved_job_offer_rate.rate == 3


@pytest.mark.django_db
def test_update_job_offer_rate(repository, job_offer, user):
    job_offer_rate_data = {
        "job_offer": job_offer,
        "rate": 2,
    }
    created_job_offer_rate = repository.create(job_offer_rate_data)

    updated_data = {"rate": 1}
    updated_job_offer_rate = repository.update(created_job_offer_rate.id, updated_data)

    assert updated_job_offer_rate is not None
    assert updated_job_offer_rate.rate == 1


@pytest.mark.django_db
def test_delete_job_offer_rate(repository, job_offer, user):
    job_offer_rate_data = {
        "job_offer": job_offer,
        "rate": 4,
    }
    created_job_offer_rate = repository.create(job_offer_rate_data)

    repository.delete(created_job_offer_rate.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_job_offer_rate.id)
