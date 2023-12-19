# import pytest
# from rest_framework.test import APIRequestFactory
# from payment.views import SuccessView, CancelView
#
# factory = APIRequestFactory()
#
#
# @pytest.mark.django_db
# def test_success_return_success_view():
#     request = factory.get("/payment/success")
#     response = SuccessView.as_view()(request)
#     assert response.status_code == 200
#
#
# @pytest.mark.django_db
# def test_success_return_cancel_view():
#     request = factory.get("/payment/cancel")
#     response = CancelView.as_view()(request)
#     assert response.status_code == 200
