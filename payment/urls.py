from django.urls import path
from .views import StripeCheckoutSessionView, stripe_webhook, SuccessView, CancelView, StripeIntentView

urlpatterns = [
    path("new_company/", StripeCheckoutSessionView.as_view(), name="new_company_checkout"),
    path("new_company/success/", SuccessView.as_view(), name="success"),
    path("new_company/cancel/", CancelView.as_view(), name="cancel"),
    path("new_company/webhook/", stripe_webhook, name="new_company_webhook"),
    path("new_company/intent/<pk>/", StripeIntentView.as_view(), name="create_payment_intent")
]
