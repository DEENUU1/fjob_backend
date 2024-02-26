import pytest
from rest_framework.exceptions import NotFound

from support.models import Contact
from support.repository.contact_repository import ContactRepository


@pytest.fixture
def repository():
    return ContactRepository()


@pytest.mark.django_db
def test_create(repository):
    contact_data = {
        "subject": "Test Subject",
        "message": "Test Message",
        "email": "test@example.com"
    }

    created_contact = repository.create(contact_data)

    assert isinstance(created_contact, Contact)
    assert created_contact.subject == "Test Subject"
    assert created_contact.message == "Test Message"
    assert created_contact.email == "test@example.com"


@pytest.mark.django_db
def test_get_all(repository):
    contacts_data = [
        {"subject": "Subject 1", "message": "Message 1", "email": "email1@example.com"},
        {"subject": "Subject 2", "message": "Message 2", "email": "email2@example.com"}
    ]

    created_contacts = [repository.create(contact) for contact in contacts_data]
    retrieved_contacts = repository.get_all()

    assert len(retrieved_contacts) == 2
    assert set(retrieved_contacts) == set(created_contacts)


@pytest.mark.django_db
def test_get_by_id(repository):
    contact_data = {
        "subject": "Test Subject",
        "message": "Test Message",
        "email": "test@example.com"
    }

    created_contact = repository.create(contact_data)
    retrieved_contact = repository.get_by_id(created_contact.id)

    assert retrieved_contact == created_contact


@pytest.mark.django_db
def test_get_by_id_not_found(repository):
    with pytest.raises(NotFound):
        repository.get_by_id(999)  # Assuming ID 999 doesn't exist


@pytest.mark.django_db
def test_update(repository):
    contact_data = {
        "subject": "Test Subject",
        "message": "Test Message",
        "email": "test@example.com"
    }
    updated_data = {"subject": "Updated Subject"}

    created_contact = repository.create(contact_data)
    updated_contact = repository.update(created_contact.id, updated_data)

    assert updated_contact.subject == "Updated Subject"


@pytest.mark.django_db
def test_update_not_found(repository):
    with pytest.raises(NotFound):
        repository.update(999, {"subject": "Updated Subject"})  # Assuming ID 999 doesn't exist


@pytest.mark.django_db
def test_delete(repository):
    contact_data = {
        "subject": "Test Subject",
        "message": "Test Message",
        "email": "test@example.com"
    }

    created_contact = repository.create(contact_data)
    repository.delete(created_contact.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_contact.id)


@pytest.mark.django_db
def test_delete_not_found(repository):
    with pytest.raises(NotFound):
        repository.delete(999)  # Assuming ID 999 doesn't exist
