class PaymentService:
    """
    Service class for handling payment-related operations.

    Methods:
    - create_checkout_session(stripe, product, company_id: int, request, success_url: str, cancel_url: str) -> str:
        Creates a checkout session for a product using Stripe.

        Parameters:
        - stripe: The Stripe API client.
        - product: The product for which the checkout session is created.
        - company_id (int): The ID of the company associated with the product.
        - request: The HTTP request object.
        - success_url (str): The URL to redirect to upon successful payment.
        - cancel_url (str): The URL to redirect to upon canceled payment.

        Returns:
        - str: The URL of the created checkout session.
    """

    @staticmethod
    def create_checkout_session(stripe, product, company_id: int, request, success_url: str, cancel_url: str) -> str:
        """
        Creates a checkout session for a product using Stripe.

        Parameters:
        - stripe: The Stripe API client.
        - product: The product for which the checkout session is created.
        - company_id (int): The ID of the company associated with the product.
        - request: The HTTP request object.
        - success_url (str): The URL to redirect to upon successful payment.
        - cancel_url (str): The URL to redirect to upon canceled payment.

        Returns:
        - str: The URL of the created checkout session.
        """
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
        return checkout_session.url
