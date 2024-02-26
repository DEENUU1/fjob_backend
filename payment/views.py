import json

import stripe
from django.conf import settings
from django.http import HttpResponse
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from company.repository.company_repository import CompanyRepository
from company.services.company import CompanyService
from payment.repository.product_repository import ProductRepository
from payment.services.payment import PaymentService
from payment.services.product import ProductService
from .models import Product
from .serializers import OutputProductListSerializer

stripe.api_key = settings.STRIPE_SECRET_KEY


class ProductListAPIView(APIView):
    """
    API view for listing all products.

    Attributes:
    - _service: An instance of the ProductService for handling product-related operations.
    """

    _service = ProductService(ProductRepository())

    def get(self):
        """
        Handles the HTTP GET request to retrieve a list of all products.

        Returns:
        - Response: The serialized data of all products.
        """
        products = self._service.get_all()
        serializer = OutputProductListSerializer(products, many=True)
        return Response(serializer.data)


class StripeCheckoutSessionView(APIView):
    """
    API view for creating a Stripe checkout session.

    Attributes:
    - permission_classes: The permissions required for accessing this view.
    - _service: An instance of the PaymentService for handling payment-related operations.
    """

    permission_classes = (IsAuthenticated,)
    _service = PaymentService()

    def post(self, request):
        """
        Handles the HTTP POST request to create a Stripe checkout session.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The serialized data of the created checkout session.
        """
        success_url = request.build_absolute_uri(reverse("success"))
        cancel_url = request.build_absolute_uri(reverse("cancel"))

        product_id = self.request.data.get("product_id", None)

        if product_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        company_id = self.request.data.get("company_id", None)
        product = Product.objects.get(id=product_id)

        # If product type is "NEW_OFFER" but company_id is None, it should return bad request
        if product.type == "NEW_OFFER" and company_id is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        checkout_session = self._service.create_checkout_session(
            stripe,
            product,
            company_id,
            self.request,
            success_url,
            cancel_url
        )

        return Response({"id": checkout_session})


@csrf_exempt
def stripe_webhook(request):
    """
    Webhook endpoint for processing Stripe events.

    Parameters:
    - request: The HTTP request object.

    Returns:
    - HttpResponse: An HTTP response indicating the success of the webhook processing.
    """
    payload = request.body
    sig_header = request.META["HTTP_STRIPE_SIGNATURE"]

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET
        )
    except ValueError:
        return Response(status=status.HTTP_400_BAD_REQUEST)

    if event["type"] == "checkout.session.completed" or event["type"] == "payment_intent.succeeded":
        session = event["data"]["object"]
        purchase_type = session.metadata["type"]
        value = session.metadata["value"]

        # If payment is success, increment the number of available offers with a given value
        if purchase_type == "NEW_OFFER":
            company_id = session.metadata["company_id"]
            _service = CompanyService(CompanyRepository())
            _service.increment_num_of_available_offers(company_id, int(value))

    return HttpResponse(status=status.HTTP_200_OK)


class StripeIntentView(APIView):
    """
    API view for creating a Stripe payment intent.

    """

    def post(self, request, *args, **kwargs):
        """
        Handles the HTTP POST request to create a Stripe payment intent.

        Parameters:
        - request: The HTTP request object.

        Returns:
        - Response: The serialized data of the created payment intent.
        """
        req_json = json.loads(request.body)
        customer = stripe.Customer.create(email=req_json["email"])
        intent = stripe.PaymentIntent.create(
            amount=req_json["amount_total"],
            currency=req_json["currency"],
            customer=customer["id"],
        )
        return Response({"client_secret": intent["client_secret"]})


class SuccessView(APIView):
    """
    API view for indicating a successful transaction.

    """

    def get(self, request):
        """
        Handles the HTTP GET request indicating a successful transaction.

        Returns:
        - Response: A success message.
        """
        return Response({"info": "Success!"})


class CancelView(APIView):
    """
    API view for indicating a canceled transaction.

    """

    def get(self, request):
        """
        Handles the HTTP GET request indicating a canceled transaction.

        Returns:
        - Response: A cancellation message.
        """
        return Response({"info": "Cancel!"})
