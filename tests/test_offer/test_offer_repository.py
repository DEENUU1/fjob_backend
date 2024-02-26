import pytest

from location.models import Address
from offer.models import JobOffer, EmploymentType, WorkType, Experience, Salary
from offer.repository.offer_repository import OfferRepository


@pytest.fixture
def repository():
    return OfferRepository()


@pytest.mark.django_db
def test_create_addresses(repository):
    addresses_data = [
        {"country": "Country1", "region": "Region1", "city": "City1", "street": "Street1"},
        {"country": "Country2", "region": "Region2", "city": "City2", "street": "Street2"},
    ]

    created_addresses = repository.create_addresses(addresses_data)

    assert len(created_addresses) == 2
    assert isinstance(created_addresses[0], Address)
    assert created_addresses[0].country.name == "Country1"
    assert created_addresses[1].region.name == "Region2"


@pytest.mark.django_db
def test_create_salary(repository):
    salaries_data = [
        {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"},
        {"salary_from": 80000, "salary_to": 100000, "currency": "EUR", "schedule": "Part-time"},
    ]

    created_salaries = repository.create_salary(salaries_data)

    assert len(created_salaries) == 2
    assert isinstance(created_salaries[0], Salary)
    assert created_salaries[0].salary_from == 50000
    assert created_salaries[1].schedule == "Part-time"


@pytest.mark.django_db
def test_create_employment_type(repository):
    employment_types_data = ["Full-time", "Contract"]

    created_employment_types = repository.create_employment_type(employment_types_data)

    assert len(created_employment_types) == 2
    assert isinstance(created_employment_types[0], EmploymentType)
    assert created_employment_types[0].name == "Full-time"
    assert created_employment_types[1].name == "Contract"


@pytest.mark.django_db
def test_create_work_type(repository):
    work_types_data = ["Remote", "On-site"]

    created_work_types = repository.create_work_type(work_types_data)

    assert len(created_work_types) == 2
    assert isinstance(created_work_types[0], WorkType)
    assert created_work_types[0].name == "Remote"
    assert created_work_types[1].name == "On-site"


@pytest.mark.django_db
def test_create_experience(repository):
    experiences_data = ["Entry-level", "Senior"]

    created_experiences = repository.create_experience(experiences_data)

    assert len(created_experiences) == 2
    assert isinstance(created_experiences[0], Experience)
    assert created_experiences[0].name == "Entry-level"
    assert created_experiences[1].name == "Senior"


@pytest.mark.django_db
def test_create_offer(repository):
    employment_types_data = ["Full-time", "Contract"]
    work_types_data = ["Remote", "On-site"]
    experiences_data = ["Entry-level", "Senior"]
    salaries_data = [
        {"salary_from": 50000, "salary_to": 70000, "currency": "USD", "schedule": "Full-time"},
        {"salary_from": 80000, "salary_to": 100000, "currency": "EUR", "schedule": "Part-time"},
    ]
    addresses_data = [
        {"country": "Country1", "region": "Region1", "city": "City1", "street": "Street1"},
        {"country": "Country2", "region": "Region2", "city": "City2", "street": "Street2"},
    ]

    repository.create_offer(
        employment_type=employment_types_data,
        work_type=work_types_data,
        experience=experiences_data,
        salaries=salaries_data,
        addresses=addresses_data,
        title="Job Title",
        description="Job Description",
        is_remote=True,
        is_hybrid=False,
        skills="Python, Django",
        company_logo="https://example.com/logo.png",
        company_name="Example Inc.",
        url="https://example.com/job-offer",
    )

    offer = JobOffer.objects.first()
    assert offer.title == "Job Title"
    assert offer.description == "Job Description"
    assert offer.is_remote is True
    assert offer.is_hybrid is False
    assert offer.skills == "Python, Django"
    assert offer.company_logo == "https://example.com/logo.png"
    assert offer.company_name == "Example Inc."
    assert offer.url == "https://example.com/job-offer"

    assert offer.employment_type.count() == 2
    assert offer.work_type.count() == 2
    assert offer.experience.count() == 2
    assert offer.salary.count() == 2
    assert offer.addresses.count() == 2
