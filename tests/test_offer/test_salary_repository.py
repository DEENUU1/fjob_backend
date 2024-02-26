import pytest
from rest_framework.exceptions import NotFound

from offer.models import Salary
from offer.repository.salary_repository import SalaryRepository


@pytest.fixture
def repository():
    return SalaryRepository()


@pytest.mark.django_db
def test_create(repository):
    salary_data = {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"}

    created_salary = repository.create(salary_data)

    assert isinstance(created_salary, Salary)
    assert created_salary.salary_from == 50000
    assert created_salary.schedule == "Full-time"


@pytest.mark.django_db
def test_get_by_id(repository):
    salary_data = {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"}

    created_salary = repository.create(salary_data)
    retrieved_salary = repository.get_by_id(created_salary.id)

    assert retrieved_salary == created_salary


@pytest.mark.django_db
def test_get_by_id_not_found(repository):
    with pytest.raises(NotFound):
        repository.get_by_id(999)


@pytest.mark.django_db
def test_update(repository):
    salary_data = {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"}
    updated_data = {"salary_from": 60000, "currency": "EUR"}

    created_salary = repository.create(salary_data)
    updated_salary = repository.update(created_salary.id, updated_data)

    assert updated_salary.salary_from == 60000
    assert updated_salary.currency == "EUR"


@pytest.mark.django_db
def test_update_not_found(repository):
    with pytest.raises(NotFound):
        repository.update(999, {"salary_from": 60000, "currency": "EUR"})


@pytest.mark.django_db
def test_delete(repository):
    salary_data = {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"}

    created_salary = repository.create(salary_data)
    repository.delete(created_salary.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_salary.id)


@pytest.mark.django_db
def test_delete_not_found(repository):
    with pytest.raises(NotFound):
        repository.delete(999)
