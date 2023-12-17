import pytest
from tests.fixtures import user, user_no_available_companies, company, user_second
from rest_framework.test import force_authenticate, APIRequestFactory
from company.views import UserCanMakeCompanyView, CompanyOfferListView, UserHasCompanyView, CompanyPublicView, CompanyUserView
from users.models import UserAccount
from company.models import Company
import json


factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_check_if_user_is_able_to_create_company_return_true(user):
    view = UserCanMakeCompanyView.as_view()

    request = factory.get('/api/company/user/check/new')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert response.data["info"] == "true"


@pytest.mark.django_db
def test_success_check_if_user_is_not_able_to_create_company_return_false(user_no_available_companies):
    view = UserCanMakeCompanyView.as_view()

    request = factory.get('/api/company/user/check/new')
    force_authenticate(request, user=user_no_available_companies)
    response = view(request)

    assert response.status_code == 200
    assert response.data["info"] == "false"


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
def test_success_return_true_if_user_has_company(user, company):
    view = UserHasCompanyView.as_view()
    request = factory.get("/api/company/user/check/company")
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert response.data["info"] == "true"


@pytest.mark.django_db
def test_success_company_public_return_list_of_companies(company):
    view = CompanyPublicView.as_view({"get": "list"})
    request = factory.get("/api/company/")
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 0


# @pytest.mark.django_db
# def test_success_company_public_return_company_by_id(company):
#     view = CompanyPublicView.as_view({"get": "retrieve"})
#     request = factory.get("/api/company/1/")
#     response = view(request, 1)
#
#     assert response.status_code == 200
#     assert response.data["id"] == 1
#

@pytest.mark.django_db
def test_error_company_public_return_company_by_id_not_found(company):
    view = CompanyPublicView.as_view({"get": "retrieve"})
    request = factory.get("/api/company/2/")
    response = view(request)

    assert response.status_code == 404


@pytest.mark.django_db
def test_success_ist_user_companies(user, company):
    view = CompanyUserView.as_view({'get': 'list'})

    request = factory.get('/api/company/management/')
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]['id'] == company.id


@pytest.mark.django_db
def test_success_retrieve_company_details(user, company):
    view = CompanyUserView.as_view({'get': 'retrieve'})

    request = factory.get('/api/company/management/1/')
    force_authenticate(request, user=user)
    response = view(request, pk=company.id)

    assert response.status_code == 200
    assert response.data['id'] == company.id


@pytest.mark.django_db
def test_error_create_company_exceeds_limit(user):
    view = CompanyUserView.as_view({'post': 'create'})

    user.num_of_available_companies = 0
    user.save()

    data = {'name': 'New Company', 'description': 'A test company'}

    request = factory.post('/api/company/management/', data)
    force_authenticate(request, user=user)
    response = view(request)

    assert response.status_code == 400
    assert response.data['info'] == 'You have reached the limit of Companies. Pay to make more'


@pytest.mark.django_db
def test_success_partial_update_company(user, company):
    view = CompanyUserView.as_view({'patch': 'partial_update'})

    data = {'description': 'Updated description'}

    request = factory.patch('/api/company/management/1/', data)
    force_authenticate(request, user=user)
    response = view(request, pk=company.id)

    assert response.status_code == 200
    assert response.data['description'] == 'Updated description'


@pytest.mark.django_db
def test_success_destroy_company(user, company):
    view = CompanyUserView.as_view({'delete': 'destroy'})

    request = factory.delete('/api/company/management/1/')
    force_authenticate(request, user=user)
    response = view(request, pk=company.id)

    assert response.status_code == 204
    assert not Company.objects.filter(id=company.id, is_active=True).exists()

