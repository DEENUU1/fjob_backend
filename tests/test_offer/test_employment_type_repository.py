import pytest
from rest_framework.exceptions import NotFound

from offer.repository.employment_type_repository import EmploymentTypeRepository


@pytest.fixture
def repository():
    return EmploymentTypeRepository()


@pytest.mark.django_db
def test_create_employment_type(repository):
    employment_type_data = {
        "name": "Full-Time",
    }
    employment_type = repository.create(employment_type_data)
    assert employment_type.id is not None
    assert employment_type.name == "Full-Time"


@pytest.mark.django_db
def test_get_employment_type_by_id(repository):
    employment_type_data = {
        "name": "Contract",
    }
    created_employment_type = repository.create(employment_type_data)

    retrieved_employment_type = repository.get_by_id(created_employment_type.id)
    assert retrieved_employment_type is not None
    assert retrieved_employment_type.name == "Contract"


@pytest.mark.django_db
def test_update_employment_type(repository):
    employment_type_data = {
        "name": "Temporary",
    }
    created_employment_type = repository.create(employment_type_data)

    updated_data = {"name": "Fixed-Term"}
    updated_employment_type = repository.update(created_employment_type.id, updated_data)

    assert updated_employment_type is not None
    assert updated_employment_type.name == "Fixed-Term"


@pytest.mark.django_db
def test_delete_employment_type(repository):
    employment_type_data = {
        "name": "Internship",
    }
    created_employment_type = repository.create(employment_type_data)

    repository.delete(created_employment_type.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_employment_type.id)
