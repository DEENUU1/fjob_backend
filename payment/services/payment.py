

class PaymentService:

    @staticmethod
    def create_checkout_session(stripe, product, company_id: int, request, success_url: str, cancel_url: str) -> str:
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
