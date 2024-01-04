import json

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.models import Company
from .models import Product
from .serializers import ProductListSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListView(ListAPIView):
    # Return list of available products
    queryset = Product.objects.all()
    serializer_class = ProductListSerializer


class StripeCheckoutSessionView(APIView):
    # Create checkout session
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Get success and cancel endpoints
        success_url = request.build_absolute_uri(reverse("success"))
        cancel_url = request.build_absolute_uri(reverse("cancel"))

        # Get product_id and company_id
        data = self.request.data
        product_id = data.get("product_id", None)
        company_id = data.get("company_id", None)

        if product_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(id=product_id)
        # If product type is "NEW_OFFER" but company_id is None it should return bad request
        if product.type == "NEW_OFFER" and company_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        # Create checkout session
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[
                {
                    "price": product.price_euro_id,
                    "quantity": 1
                }
            ],
            mode="payment",
            metadata={
                "company_id": company_id,
                "type": product.type,
                "value": product.value,
                "product_id": product.id,
                "user_id": request.user.id
            },
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return Response({"id": checkout_session.url})


def increment_num_of_available_offers(session, value):
    company_id = session.metadata["company_id"]
    company = Company.objects.get(id=company_id)
    company.num_of_offers_to_add += int(value)
    company.save()


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event["type"] == "checkout.session.completed" or event["type"] == "payment_intent.succeeded":
        session = event["data"]["object"]
        purchase_type = session.metadata["type"]
        value = session.metadata["value"]

        # If payment is success increment number of available offers with a given value
        if purchase_type == "NEW_OFFER":
            increment_num_of_available_offers(session, value)

    return HttpResponse(status=status.HTTP_200_OK)


class StripeIntentView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            req_json = json.loads(request.body)
            customer = stripe.Customer.create(email=req_json["email"])
            intent = stripe.PaymentIntent.create(
                amount=req_json["amount_total"],
                currency=req_json["currency"],
                customer=customer["id"],
            )
            return Response({"client_secret": intent["client_secret"]})
        except:
            return Response({"error": "Something went wrong"})


class SuccessView(APIView):
    def get(self, request):
        return Response({"info": "Success!"})


class CancelView(APIView):
    def get(self, request):
        return Response({"info": "Cancel!"})
