import pytest
from tests.fixtures import user, user_no_available_companies, company, user_second
from rest_framework.test import force_authenticate, APIRequestFactory
from company.views import UserCanMakeCompanyView, CompanyOfferListView, UserHasCompanyView, CompanyPublicView

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
    assert len(response.data) == 1


@pytest.mark.django_db
def test_success_company_public_return_company_by_id(company):
    view = CompanyPublicView.as_view({"get": "retrieve"})
    request = factory.get("/api/company/1/")
    response = view(request, 1)

    assert response.status_code == 200
    assert response.data["id"] == 1


@pytest.mark.django_db
def test_error_company_public_return_company_by_id_not_found(company):
    view = CompanyPublicView.as_view({"get": "retrieve"})
    request = factory.get("/api/company/2/")
    response = view(request)

    assert response.status_code == 404
