from django.urls import path
from .views import NewCompanySuccessView, NewCompanyCancelView, NewCompanyCreateCheckoutSessionView


urlpatterns = [
    path("new_company/", NewCompanyCreateCheckoutSessionView.as_view(), name="new_company"),
    path("new_company/success/", NewCompanySuccessView.as_view(), name="new_company_success"),
    path("new_company/cancel/", NewCompanyCancelView.as_view(), name="new_company_cancel"),
]
