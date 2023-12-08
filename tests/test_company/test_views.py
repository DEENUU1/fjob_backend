import pytest
from tests.fixtures import user, user_no_available_companies, company, user_second
from rest_framework.test import force_authenticate, APIRequestFactory
from company.views import UserCanMakeCompanyView, CompanyOfferListView

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
