import pytest
from rest_framework.test import APIRequestFactory

from offer.models import WorkType, EmploymentType, Experience, Salary
from offer.views import (
    OfferListView,
    SalaryView,
    ExperienceListAPIView,
    EmploymentTypeListAPIView,
    WorkTypeListAPIView
)
from tests.fixtures import user, job_offer, job_offer_with_company, company

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_return_list_of_work_type():
    WorkType.objects.create(name='test_work_type_1')
    WorkType.objects.create(name='test_work_type_2')

    request = factory.get('/offer/work_type/')
    view = WorkTypeListAPIView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_list_of_employment_type():
    EmploymentType.objects.create(name='test_employment_type_1')
    EmploymentType.objects.create(name='test_employment_type_2')

    request = factory.get('/offer/employment_type/')
    view = EmploymentTypeListAPIView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_list_of_experience():
    Experience.objects.create(name='test_experience_1')
    Experience.objects.create(name='test_experience_2')

    request = factory.get('/offer/experience/')
    view = ExperienceListAPIView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_min_max_salary():
    Salary.objects.create(salary_from=1000, salary_to=2000, currency="PLN", schedule="MONTHLY")
    Salary.objects.create(salary_from=3000, salary_to=4000, currency="PLN", schedule="MONTHLY")

    request = factory.get('/offer/salary/')
    view = SalaryView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data['min'] == 1000.0
    assert response.data['max'] == 4000.0


@pytest.mark.django_db
def test_success_return_min_max_salary_empty():
    request = factory.get('/offer/salary/')
    view = SalaryView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data is None


@pytest.mark.django_db
def test_success_return_list_of_job_offers(user, job_offer, job_offer_with_company, company):
    request = factory.get('/offer/')
    view = OfferListView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 4
