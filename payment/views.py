from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from users.models import UserAccount
from django.urls import reverse
from rest_framework.permissions import IsAuthenticated
from .models import Product
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import HttpResponse
from company.models import Company

stripe.api_key = settings.STRIPE_SECRET_KEY


class StripeCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        success_url = request.build_absolute_uri(reverse("success"))
        cancel_url = request.build_absolute_uri(reverse("cancel"))
        product_id = self.kwargs.get("pk", None)
        company_id = self.kwargs.get("company_id", None)

        if product_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(product_id)
        if product.type == "NEW_OFFER" and company_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

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
                "product_id": product.id,
                "user_id": request.user.id
            },
            success_url=success_url,
            cancel_url=cancel_url,
        )
        return Response({"id": checkout_session.id})


def increment_num_of_available_companies(session, value):
    user_id = session.metadata["user_id"]
    user = UserAccount.objects.get(id=user_id)
    user.num_of_available_companies += value
    user.save()


def increment_num_of_available_offers(session, value):
    company_id = session.metada["company_id"]
    company = Company.objects.get(id=company_id)
    company.num_of_available_offers += value
    company.save()


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    except stripe.error.SignatureVerificationError as e:
        print(e)
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event["type"] == "checkout.session.completed" or event["type"] == "payment_intent.succeeded":
        session = event["data"]["object"]
        # Todo customer_email = session.customer_details["email"], send_email

        purchase_type = session.metadata["type"]
        value = session.metadata["session"]

        if purchase_type == "NEW_COMPANY":
            increment_num_of_available_companies(session, value)
        elif purchase_type == "NEW_OFFER":
            increment_num_of_available_offers(session, value)

    return HttpResponse(status=status.HTTP_200_OK)


class SuccessView(APIView):
    def get(self, request):
        return Response({"info": "Success!"})


class CancelView(APIView):
    def get(self, request):
        return Response({"info": "Cancel!"})


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
        except Exception as e:
            return Response({"error": "Something went wrong"})