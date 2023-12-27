from django.urls import path

from .views import StripeCheckoutSessionView, stripe_webhook, SuccessView, CancelView, StripeIntentView, ProductListView

urlpatterns = [
    path("product/", ProductListView.as_view(), name="new_offer_product_list"),
    path("", StripeCheckoutSessionView.as_view(), name="new_company_checkout"),
    path("success/", SuccessView.as_view(), name="success"),
    path("cancel/", CancelView.as_view(), name="cancel"),
    path("webhook/", stripe_webhook, name="new_company_webhook"),
    path("intent/<int:pk>/company_id/", StripeIntentView.as_view(), name="create_payment_intent")
]
