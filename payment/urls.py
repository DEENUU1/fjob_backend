from django.urls import path
from .views import NewCompanyCheckoutSessionView, stripe_webhook, SuccessView, CancelView, StripeIntentView

urlpatterns = [
    path("new_company/", NewCompanyCheckoutSessionView.as_view(), name="new_company_checkout"),
    path("new_company/success/", SuccessView.as_view(), name="new_company_success"),
    path("new_company/cancel/", CancelView.as_view(), name="new_company_cancel"),
    path("new_company/webhook/", stripe_webhook, name="new_company_webhook"),
    path("new_company/intent/<pk>/", StripeIntentView.as_view(), name="create_payment_intent")
]
