import pytest
from rest_framework.exceptions import NotFound

from company.repository.company_repository import CompanyRepository
from users.models import UserAccount


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name="test", last_name="user", email="test@example.com")


@pytest.fixture
def repository():
    return CompanyRepository()


@pytest.mark.django_db
def test_create_company(repository, user):
    company_data = {
        "name": "Test Company",
        "slug": "test-company",
        "category": None,
        "logo": None,
        "company_size": "Small",
        "description": "A test company",
        "user": user,
        "num_of_offers_to_add": 1,
        "is_active": True,
    }
    company = repository.create(company_data)
    assert company.id is not None
    assert company.name == "Test Company"
    assert company.slug == "1-test-company"


@pytest.mark.django_db
def test_get_all_companies(repository, user):
    companies = repository.get_all()
    assert len(companies) == 0

    company_data = {
        "name": "Another Company",
        "slug": "another-company",
        "category": None,
        "logo": None,
        "company_size": "Medium",
        "description": "Another test company",
        "user": user,
        "num_of_offers_to_add": 2,
        "is_active": True,
    }
    repository.create(company_data)

    companies = repository.get_all()
    assert len(companies) == 1
    assert companies[0].name == "Another Company"
    assert companies[0].slug == "1-another-company"


@pytest.mark.django_db
def test_get_company_by_id(repository, user):
    company_data = {
        "name": "Test Company",
        "slug": "test-company",
        "category": None,
        "logo": None,
        "company_size": "Small",
        "description": "A test company",
        "user": user,
        "num_of_offers_to_add": 1,
        "is_active": True,
    }
    created_company = repository.create(company_data)

    retrieved_company = repository.get_by_id(created_company.id)
    assert retrieved_company is not None
    assert retrieved_company.name == "Test Company"
    assert retrieved_company.slug == "1-test-company"


@pytest.mark.django_db
def test_update_company(repository, user):
    company_data = {
        "name": "Test Company",
        "slug": "test-company",
        "category": None,
        "logo": None,
        "company_size": "Small",
        "description": "A test company",
        "user": user,
        "num_of_offers_to_add": 1,
        "is_active": True,
    }
    created_company = repository.create(company_data)

    updated_data = {"name": "Updated Company", "is_active": False}
    updated_company = repository.update(created_company.id, updated_data)

    assert updated_company is not None
    assert updated_company.name == "Updated Company"
    assert not updated_company.is_active


@pytest.mark.django_db
def test_delete_company(repository, user):
    company_data = {
        "name": "Test Company",
        "slug": "test-company",
        "category": None,
        "logo": None,
        "company_size": "Small",
        "description": "A test company",
        "user": user,
        "num_of_offers_to_add": 1,
        "is_active": True,
    }
    created_company = repository.create(company_data)

    repository.delete(created_company.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_company.id)


@pytest.mark.django_db
def test_get_all_active_companies(repository, user):
    active_company_data = {
        "name": "Active Company",
        "slug": "active-company",
        "user": user,
        "num_of_offers_to_add": 3,
        "is_active": True,
    }
    repository.create(active_company_data)

    inactive_company_data = {
        "name": "Inactive Company",
        "slug": "inactive-company",
        "user": user,
        "num_of_offers_to_add": 2,
        "is_active": False,
    }
    repository.create(inactive_company_data)

    active_companies = repository.get_all_active()
    assert len(active_companies) == 1
    assert active_companies[0].name == "Active Company"
    assert active_companies[0].is_active

@pytest.mark.django_db
def test_get_active_company_by_slug(repository, user):
    company_data = {
        "name": "Active Company",
        "slug": "active-company",
        "user": user,
        "num_of_offers_to_add": 3,
        "is_active": True,
    }
    repository.create(company_data)

    active_company = repository.get_active_by_slug("1-active-company")
    assert active_company.name == "Active Company"
    assert active_company.is_active

    non_existent_company = repository.get_active_by_slug("non-existent-company")
    assert non_existent_company is None

@pytest.mark.django_db
def test_get_company_by_user(repository, user):
    company_data = {
        "name": "User's Company",
        "slug": "users-company",
        "user": user,
        "num_of_offers_to_add": 5,
        "is_active": True,
    }
    repository.create(company_data)

    user_company = repository.get_company_by_user(user)
    assert user_company.name == "User's Company"
    assert user_company.user == user

    another_user = UserAccount.objects.create(first_name="another", last_name="user", email="another@gmail.com")
    non_user_company = repository.get_company_by_user(another_user)
    assert non_user_company is None

@pytest.mark.django_db
def test_increment_num_of_available_offers(repository, user):
    company_data = {
        "name": "Test Company",
        "slug": "test-company",
        "user": user,
        "num_of_offers_to_add": 3,
        "is_active": True,
    }
    created_company = repository.create(company_data)

    repository.increment_num_of_available_offers(created_company.id, 2)
    updated_company = repository.get_by_id(created_company.id)

    assert updated_company is not None
    assert updated_company.num_of_offers_to_add == 5

    repository.increment_num_of_available_offers(created_company.id, -1)
    updated_company = repository.get_by_id(created_company.id)

    assert updated_company is not None
    assert updated_company.num_of_offers_to_add == 4