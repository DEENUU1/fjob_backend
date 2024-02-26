import pytest
from rest_framework.test import APIRequestFactory, force_authenticate

from company.models import Company, CompanyCategory
from company.views import (
    CompanyCategoryListView,
    CompanyPublicListAPIView,
    CompanyPublicRetrieveAPIView,
    UserCompanyView
)
from users.models import UserAccount

factory = APIRequestFactory()


@pytest.fixture
def user():
    return UserAccount.objects.create(first_name='XXXX', last_name="xxx", email='XXXXXXXXXXXXX')


@pytest.mark.django_db
def test_company_category_list_view_success():
    CompanyCategory.objects.create(name='test')
    request = factory.get('api/offer/category/')
    view = CompanyCategoryListView.as_view()
    response = view(request)
    assert response.status_code == 200


@pytest.mark.django_db
def test_company_public_list_api_view_success(user):
    Company.objects.create(name='test', is_active=True, user=user)
    Company.objects.create(name='test2', is_active=False, user=user)
    request = factory.get('api/company/')
    view = CompanyPublicListAPIView.as_view()
    response = view(request)
    assert response.status_code == 200
    assert len(response.data) == 1


@pytest.mark.django_db
def test_company_public_retrieve_api_view_success(user):
    Company.objects.create(name='test', is_active=True, user=user)
    request = factory.get('api/company/1-test/')
    view = CompanyPublicRetrieveAPIView.as_view()
    response = view(request, slug="1-test")
    assert response.status_code == 200
    assert response.data['name'] == 'test'


@pytest.mark.django_db
def test_user_company_view_error_unauthorized_user(user):
    Company.objects.create(name="test", is_active=True, user=user)
    request = factory.get('api/company/')
    view = UserCompanyView.as_view()
    response = view(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_user_company_view_success(user):
    Company.objects.create(name="test", is_active=True, user=user)
    request = factory.get('api/company/')
    force_authenticate(request, user=user)
    view = UserCompanyView.as_view()
    response = view(request)
    assert response.status_code == 200
