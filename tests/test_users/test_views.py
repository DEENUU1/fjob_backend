import pytest
from tests.fixtures import user, job_offer, job_offer_with_company, user_second, company
from rest_framework.test import force_authenticate, APIRequestFactory
from users.views import GetUserNumOfAvailableCompaniesView
import json
from users.models import UserAccount

factory = APIRequestFactory()


# @pytest.mark.django_db
# def test_success_return_number_of_available_companies_user_can_create(user):
#     request = factory.get(
#         "api/users/user/num_of_available_companies",
#     )
#     view = GetUserNumOfAvailableCompaniesView.as_view()
#     force_authenticate(request, user=user)
#     response = view(request)
#     assert response.status_code == 200
#     assert response.data == {"num_of_available_companies": 1}


# @pytest.mark.django_db
# def test_error_return_number_of_available_companies_user_can_create_not_authenticated(user):
#     request = factory.get(
#         "api/users/user/num_of_available_companies",
#     )
#     view = GetUserNumOfAvailableCompaniesView.as_view()
#     response = view(request)
#     assert response.status_code == 401
