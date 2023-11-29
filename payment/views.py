# from rest_framework.exceptions import PermissionDenied
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# import stripe
# from django.conf import settings
# from users.models import UserAccount
# from django.urls import reverse
# from rest_framework.permissions import IsAuthenticated
# from .models import UserPayment
#
# stripe.api_key = settings.STRIPE_SECRET_KEY
#
#
# class NewCompanyCheckoutSessionView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def post(self, request):
#         success_url = request.build_absolute_uri(reverse("new_company_success"))
#         cancel_url = request.build_absolute_uri(reverse("new_company_cancel"))
#
#         checkout_session = stripe.checkout.Session.create(
#             payment_method_type=["card"],
#             line_items=[
#                 {
#                     "price": settings.NEW_COMPANY_PRICE_ID,
#                     "quantity": 1,
#                 },
#             ],
#             mode="payment",
#             customer_creation="always",
#             success_url=f"{success_url}?session_id={}",
#             cancelled_url=cancel_url
#         )
#         return Response({"url": checkout_session.url})
#
#
# class NewCompanyPaymentSuccess(APIView):
#     def get(self, request):
#         checkout_session_id = request.GET.get("session_id", None)
#         session = stripe.checkout.Session.retrieve(checkout_session_id)
#         customer = stripe.Customer.retrieve(session.customer)
#
#         user_payment = UserPayment.objects.get(user=request.user)
#         user_payment.stripe_checkout_id = checkout_session_id
#         user_payment.save()
#
#         return Response({"info": customer})
#
#
# class NewCompanyPaymentCancel(APIView):
#     def get(self, request):
#         return Response({"info": "Payment Cancelled"})
#
#
# class NewCompanyPaymentWebHook(APIView):
#     def get(self, request):
#         payload = self.request.body
#         signature_header = request.META["HTTP_STRIPE_SIGNATURE"]
#         event = None
#         try:
#             event = stripe.Webhook.construct_event(
#                 payload, signature_header, settings.STRIPE_WEBHOOK_SECRET
#             )
#         except ValueError as e:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#         except stripe.error.SignatureVerificationError:
#             return Response(status=status.HTTP_400_BAD_REQUEST)
#
#         if event["type"] == "checkout.session.completed":
#             session = event["data"]["object"]
#             session_id = session.get("id", None)
#             user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
#             user_payment.payment_bool = True
#             user_payment.save()
#         return Response(status=status.HTTP_200_OK)
