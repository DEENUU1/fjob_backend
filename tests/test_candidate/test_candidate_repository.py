import pytest
from rest_framework.exceptions import NotFound

from candidates.repository.candidate_repository import CandidateRepository
from offer.models import JobOffer
from users.models import UserAccount


@pytest.fixture
def job_offer():
    return JobOffer.objects.create(title="Software Engineer")


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name="test", last_name="user", email="test@example.com")


@pytest.fixture
def repository(job_offer, user):
    return CandidateRepository()


@pytest.mark.django_db
def test_create_candidate(repository, job_offer, user):
    candidate_data = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    candidate = repository.create(candidate_data)
    assert candidate.id is not None
    assert candidate.first_name == "John"
    assert candidate.last_name == "Doe"


@pytest.mark.django_db
def test_get_all_candidates(repository, user, job_offer):
    candidates = repository.get_all()
    assert len(candidates) == 0

    candidate_data = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "987654321",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    repository.create(candidate_data)
    candidates = repository.get_all()
    assert len(candidates) == 1
    assert candidates[0].first_name == "Jane"
    assert candidates[0].last_name == "Doe"


@pytest.mark.django_db
def test_get_candidate_by_id(repository, job_offer, user):
    candidate_data = {
        "first_name": "Bob",
        "last_name": "Smith",
        "email": "bob.smith@example.com",
        "phone": "5551234567",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    created_candidate = repository.create(candidate_data)

    retrieved_candidate = repository.get_by_id(created_candidate.id)
    assert retrieved_candidate is not None
    assert retrieved_candidate.first_name == "Bob"
    assert retrieved_candidate.last_name == "Smith"


@pytest.mark.django_db
def test_filter_candidates_by_job_offer(repository, job_offer, user):
    candidate_data_1 = {
        "first_name": "Alice",
        "last_name": "Johnson",
        "email": "alice.johnson@example.com",
        "phone": "123987654",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    repository.create(candidate_data_1)

    job_offer_2 = JobOffer.objects.create(title="Product Manager")
    candidate_data_2 = {
        "first_name": "Charlie",
        "last_name": "Brown",
        "email": "charlie.brown@example.com",
        "phone": "987654321",
        "job_offer": job_offer_2,
        "user": user,
        "status": "PENDING",
    }
    repository.create(candidate_data_2)

    candidates = repository.filter_by_job_offer(job_offer.id)
    assert len(candidates) == 1
    assert candidates[0].first_name == "Alice"
    assert candidates[0].last_name == "Johnson"


@pytest.mark.django_db
def test_filter_candidates_by_user(repository, user):
    candidate_data_1 = {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "123456789",
        "job_offer": JobOffer.objects.create(title="Software Engineer"),
        "user": user,
        "status": "PENDING",
    }
    repository.create(candidate_data_1)

    user_2 = UserAccount.objects.create(first_name="another", last_name="user", email="another@example.com")
    candidate_data_2 = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
        "phone": "987654321",
        "job_offer": JobOffer.objects.create(title="Software Engineer"),
        "user": user_2,
        "status": "PENDING",
    }
    repository.create(candidate_data_2)

    candidates = repository.filter_by_user(user)
    assert len(candidates) == 1
    assert candidates[0].first_name == "John"
    assert candidates[0].last_name == "Doe"


@pytest.mark.django_db
def test_update_candidate(repository, job_offer, user):
    candidate_data = {
        "first_name": "Tom",
        "last_name": "Johnson",
        "email": "tom.johnson@example.com",
        "phone": "123456789",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    created_candidate = repository.create(candidate_data)

    updated_data = {"first_name": "Tommy", "status": "ACCEPTED"}
    updated_candidate = repository.update(created_candidate.id, updated_data)

    assert updated_candidate is not None
    assert updated_candidate.first_name == "Tommy"
    assert updated_candidate.status == "ACCEPTED"


@pytest.mark.django_db
def test_delete_candidate(repository, job_offer, user):
    candidate_data = {
        "first_name": "James",
        "last_name": "Smith",
        "email": "james.smith@example.com",
        "phone": "987654321",
        "job_offer": job_offer,
        "user": user,
        "status": "PENDING",
    }
    created_candidate = repository.create(candidate_data)

    repository.delete(created_candidate.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_candidate.id)
