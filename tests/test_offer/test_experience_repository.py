import pytest
from rest_framework.exceptions import NotFound
from offer.models import Experience
from offer.repository.experience_repository import ExperienceRepository

@pytest.fixture
def repository():
    return ExperienceRepository()

@pytest.mark.django_db
def test_create_experience(repository):
    experience_data = {
        "name": "Entry Level",
    }
    experience = repository.create(experience_data)
    assert experience.id is not None
    assert experience.name == "Entry Level"


@pytest.mark.django_db
def test_get_experience_by_id(repository):
    experience_data = {
        "name": "Senior",
    }
    created_experience = repository.create(experience_data)

    retrieved_experience = repository.get_by_id(created_experience.id)
    assert retrieved_experience is not None
    assert retrieved_experience.name == "Senior"

@pytest.mark.django_db
def test_update_experience(repository):
    experience_data = {
        "name": "Junior",
    }
    created_experience = repository.create(experience_data)

    updated_data = {"name": "Associate"}
    updated_experience = repository.update(created_experience.id, updated_data)

    assert updated_experience is not None
    assert updated_experience.name == "Associate"

@pytest.mark.django_db
def test_delete_experience(repository):
    experience_data = {
        "name": "Intern",
    }
    created_experience = repository.create(experience_data)

    repository.delete(created_experience.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_experience.id)
