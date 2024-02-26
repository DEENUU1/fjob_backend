import pytest
from rest_framework.exceptions import NotFound

from offer.models import WorkType
from offer.repository.work_type_repository import WorkTypeRepository


@pytest.fixture
def repository():
    return WorkTypeRepository()


@pytest.mark.django_db
def test_create(repository):
    work_type_data = {"name": "Full-time"}

    created_work_type = repository.create(work_type_data)

    assert isinstance(created_work_type, WorkType)
    assert created_work_type.name == "Full-time"


@pytest.mark.django_db
def test_get_by_id(repository):
    work_type_data = {"name": "Full-time"}

    created_work_type = repository.create(work_type_data)
    retrieved_work_type = repository.get_by_id(created_work_type.id)

    assert retrieved_work_type == created_work_type


@pytest.mark.django_db
def test_get_by_id_not_found(repository):
    with pytest.raises(NotFound):
        repository.get_by_id(999)


@pytest.mark.django_db
def test_update(repository):
    work_type_data = {"name": "Full-time"}
    updated_data = {"name": "Remote"}

    created_work_type = repository.create(work_type_data)
    updated_work_type = repository.update(created_work_type.id, updated_data)

    assert updated_work_type.name == "Remote"


@pytest.mark.django_db
def test_update_not_found(repository):
    with pytest.raises(NotFound):
        repository.update(999, {"name": "Remote"})


@pytest.mark.django_db
def test_delete(repository):
    work_type_data = {"name": "Full-time"}

    created_work_type = repository.create(work_type_data)
    repository.delete(created_work_type.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_work_type.id)


@pytest.mark.django_db
def test_delete_not_found(repository):
    with pytest.raises(NotFound):
        repository.delete(999)
