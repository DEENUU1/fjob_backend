from rest_framework.views import View
from rest_framework.response import Response
from rest_framework import status
import stripe
from django.conf import settings
from users.models import UserAccount


stripe.api_key = settings.STRIPE_SECRET_KEY


class NewCompanyCreateCheckoutSessionView(View):
    def post(self, request, *args, **kwargs):
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[
                {
                    'price': settings.NEW_COMPANY_PRICE_ID,
                    'quantity': 1
                }
            ],
            mode='payment',
            success_url= ...,
            cancel_url= ...,
        )
        return Response({'url': checkout_session.url})


class NewCompanySuccessView(View):

    def get(self, request, *args, **kwargs):
        user_request = self.request.user
        user = UserAccount.objects.get(id=user_request)
        user.num_of_available_companies += 1
        user.save()
        return Response({"info": "Payment success"}, status=status.HTTP_200_OK)


class NewCompanyCancelView(View):

    def get(self, request, *args, **kwargs):
        return Response({"info": "Payment cancelled"}, status=status.HTTP_200_OK)
