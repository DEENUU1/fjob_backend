import pytest
from rest_framework.test import force_authenticate, APIRequestFactory

from company.models import Company
from company.views import CompanyOfferListView, CompanyPublicView, CompanyUserView
from tests.fixtures import user, company

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_return_list_of_offers_for_specified_company(user, company):
    view = CompanyOfferListView.as_view()
    request = factory.get("/api/company/offer/")
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200


@pytest.mark.django_db
def test_error_return_list_of_offers_for_specified_company_unauthenticated(company):
    view = CompanyOfferListView.as_view()
    request = factory.get("/api/company/offer/")
    response = view(request)

    assert response.status_code == 401


@pytest.mark.django_db
def test_success_company_public_return_list_of_companies(company):
    view = CompanyPublicView.as_view({"get": "list"})
    request = factory.get("/api/company/")
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 0


@pytest.mark.django_db
def test_error_company_public_return_company_by_id_not_found(company):
    view = CompanyPublicView.as_view({"get": "retrieve"})
    request = factory.get("/api/company/2/")
    response = view(request)

    assert response.status_code == 404


@pytest.mark.django_db
def test_success_partial_update_company(user, company):
    view = CompanyUserView.as_view()

    data = {'description': 'Updated description', "company_id": 1}

    request = factory.put('/api/company/management/', data)
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert response.data['description'] == 'Updated description'


@pytest.mark.django_db
def test_success_destroy_company(user, company):
    view = CompanyUserView.as_view()

    request = factory.delete('/api/company/management/', {"company_id": 1})
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 204
    assert not Company.objects.filter(id=company.id, is_active=True).exists()
