import pytest

from offer.models import WorkType, EmploymentType, Experience, Salary, JobOffer


@pytest.mark.django_db
def test_create_work_type_success():
    work_type = WorkType.objects.create(name='test')
    assert work_type.name == 'test'


@pytest.mark.django_db
def test_create_employment_type_success():
    employment_type = EmploymentType.objects.create(name='test')
    assert employment_type.name == 'test'


@pytest.mark.django_db
def test_create_experience_success():
    experience = Experience.objects.create(name='test')
    assert experience.name == 'test'


@pytest.mark.django_db
def test_create_salary_success():
    salary = Salary.objects.create(salary_from=1000, salary_to=2000, currency="PLN", schedule="MONTHLY")
    assert salary.salary_from == 1000
    assert salary.salary_to == 2000
    assert salary.currency == "PLN"
    assert salary.schedule == "MONTHLY"


@pytest.mark.django_db
def test_create_job_offer_success():
    joboffer = JobOffer.objects.create(title="test")
    assert joboffer.title == "test"
    assert joboffer.is_remote == False
    assert joboffer.is_hybrid == False
    assert joboffer.days_until_expiration == 30
    assert joboffer.status == "DRAFT"
