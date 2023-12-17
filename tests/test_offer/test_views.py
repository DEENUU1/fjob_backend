import pytest
from tests.fixtures import user, job_offer, job_offer_with_company, company
from rest_framework.test import APIRequestFactory
from offer.views import  OfferListView, SalaryView, ExperienceView, EmploymentTypeView, \
    WorkTypeView, JobOfferView
from offer.models import WorkType, EmploymentType, Experience, Salary


factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_return_list_of_work_type():
    WorkType.objects.create(name='test_work_type_1')
    WorkType.objects.create(name='test_work_type_2')

    request = factory.get('/offer/work_type/')
    view = WorkTypeView.as_view({"get": "list"})
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_list_of_employment_type():
    EmploymentType.objects.create(name='test_employment_type_1')
    EmploymentType.objects.create(name='test_employment_type_2')

    request = factory.get('/offer/employment_type/')
    view = EmploymentTypeView.as_view({"get": "list"})
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_list_of_experience():
    Experience.objects.create(name='test_experience_1')
    Experience.objects.create(name='test_experience_2')

    request = factory.get('/offer/experience/')
    view = ExperienceView.as_view({"get": "list"})
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 2


@pytest.mark.django_db
def test_success_return_min_max_salary():
    Salary.objects.create(salary_from=1000, salary_to=2000)
    Salary.objects.create(salary_from=3000, salary_to=4000)

    request = factory.get('/offer/salary/')
    view = SalaryView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert response.data['min'] == 1000
    assert response.data['max'] == 4000


@pytest.mark.django_db
def test_success_return_min_max_salary_empty():
    request = factory.get('/offer/salary/')
    view = SalaryView.as_view()
    response = view(request)

    assert response.status_code == 204
    assert response.data is None


@pytest.mark.django_db
def test_success_return_list_of_job_offers(user, job_offer, job_offer_with_company, company):
    request = factory.get('/offer/')
    view = OfferListView.as_view()
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 4


@pytest.mark.django_db
def test_success_return_job_offer_by_slug(job_offer, user):
    request = factory.get(f'/offer/{job_offer.slug}/')
    view = JobOfferView.as_view({"get": "retrieve"})
    response = view(request, job_offer.slug)

    assert response.status_code == 200
    assert response.data["id"] == job_offer.id
