# import pytest
# from payment.models import Product, PaymentInfo
# from tests.test_company.test_models import user_data
#
#
# @pytest.mark.django_db
# def test_create_product_success():
#     product = Product.objects.create(
#         type="NEW_COMPANY",
#         name="test product",
#         price_euro=100.10,
#         price_euro_id="asdasjdasjadsj"
#     )
#     assert product.id is not None
#     assert product.type == "NEW_COMPANY"
#     assert product.name == "test product"
#     assert product.price_euro == 100.10
#     assert product.price_euro_id == "asdasjdasjadsj"
#
#
# @pytest.mark.django_db
# def test_create_payment_info_success(user_data):
#     product = Product.objects.create(
#         type="NEW_COMPANY",
#         name="test product",
#         price_euro=100.10,
#         price_euro_id="asdasjdasjadsj"
#     )
#     payment_info = PaymentInfo.objects.create(
#         user=user_data,
#         product=product,
#         stripe_checkout_id="dasdasadsads",
#     )
#     assert payment_info.id is not None
#     assert payment_info.user == user_data
#     assert payment_info.product == product
#     assert payment_info.stripe_checkout_id == "dasdasadsads"
#     assert payment_info.payment_bool == False
