import pytest
from tests.fixtures import user, job_offer, job_offer_with_company, user_second, company
from rest_framework.test import force_authenticate, APIRequestFactory
from offer.views import CompanyOfferListView, OfferListView, SalaryView, ExperienceView, EmploymentTypeView, \
    WorkTypeView
import json
from offer.models import JobOffer, WorkType, EmploymentType, Experience, Salary

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
