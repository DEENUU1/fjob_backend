import pytest
from rest_framework.exceptions import NotFound

from offer.models import JobOffer
from support.models import Report
from support.repository.report_repository import ReportRepository
from users.models import UserAccount


@pytest.fixture
def user_instance():
    return UserAccount.objects.create(
        first_name="XXXXXXXX",
        last_name="xxx",
        email="testuser@example.com",
        password="XXXXXXXXXXXX"
    )


@pytest.fixture
def job_offer_instance():
    return JobOffer.objects.create(
        title="Test Job Offer",
    )


@pytest.fixture
def repository():
    return ReportRepository()


@pytest.mark.django_db
def test_create(repository, user_instance, job_offer_instance):
    report_data = {
        "user": user_instance,
        "offer": job_offer_instance,
        "description": "Test Description"
    }

    created_report = repository.create(report_data)

    assert isinstance(created_report, Report)
    assert created_report.user == user_instance
    assert created_report.offer == job_offer_instance
    assert created_report.description == "Test Description"


@pytest.mark.django_db
def test_get_all(repository, user_instance, job_offer_instance):
    reports_data = [
        {"user": user_instance, "offer": job_offer_instance, "description": "Description 1"},
        {"user": user_instance, "offer": job_offer_instance, "description": "Description 2"}
    ]

    created_reports = [repository.create(report) for report in reports_data]
    retrieved_reports = repository.get_all()

    assert len(retrieved_reports) == 2
    assert set(retrieved_reports) == set(created_reports)


@pytest.mark.django_db
def test_get_by_id(repository, user_instance, job_offer_instance):
    report_data = {
        "user": user_instance,
        "offer": job_offer_instance,
        "description": "Test Description"
    }

    created_report = repository.create(report_data)
    retrieved_report = repository.get_by_id(created_report.id)

    assert retrieved_report == created_report


@pytest.mark.django_db
def test_get_by_id_not_found(repository):
    with pytest.raises(NotFound):
        repository.get_by_id(999)


@pytest.mark.django_db
def test_update(repository, user_instance, job_offer_instance):
    report_data = {
        "user": user_instance,
        "offer": job_offer_instance,
        "description": "Test Description"
    }
    updated_data = {"description": "Updated Description"}

    created_report = repository.create(report_data)
    updated_report = repository.update(created_report.id, updated_data)

    assert updated_report.description == "Updated Description"


@pytest.mark.django_db
def test_update_not_found(repository):
    with pytest.raises(NotFound):
        repository.update(999, {"description": "Updated Description"})


@pytest.mark.django_db
def test_delete(repository, user_instance, job_offer_instance):
    report_data = {
        "user": user_instance,
        "offer": job_offer_instance,
        "description": "Test Description"
    }

    created_report = repository.create(report_data)
    repository.delete(created_report.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_report.id)


@pytest.mark.django_db
def test_delete_not_found(repository):
    with pytest.raises(NotFound):
        repository.delete(999)
