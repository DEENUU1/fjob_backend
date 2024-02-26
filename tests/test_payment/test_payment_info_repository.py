import pytest
from rest_framework.exceptions import NotFound

from payment.models import PaymentInfo, Product
from payment.repository.payment_info_repository import PaymentInfoRepository
from users.models import UserAccount


@pytest.fixture
def repository():
    return PaymentInfoRepository()


@pytest.fixture
def user_instance():
    return UserAccount.objects.create(first_name="John", last_name="Doe", email="john@example.com")


@pytest.fixture
def product_instance():
    return Product.objects.create(type="NEW_OFFER", name="Product 1", value=1, price_euro=10, price_euro_id="xxx")


@pytest.mark.django_db
def test_create(repository, user_instance, product_instance):
    payment_info_data = {
        "user": user_instance,  # Replace with actual user instance
        "product": product_instance,  # Replace with actual product instance
        "payment_bool": True,
        "stripe_checkout_id": "some_checkout_id"
    }

    created_payment_info = repository.create(payment_info_data)

    assert isinstance(created_payment_info, PaymentInfo)
    assert created_payment_info.user == user_instance
    assert created_payment_info.product == product_instance
    assert created_payment_info.payment_bool is True
    assert created_payment_info.stripe_checkout_id == "some_checkout_id"


@pytest.mark.django_db
def test_get_all(repository, user_instance, product_instance):
    payment_infos_data = [
        {
            "user": user_instance,
            "product": product_instance,
            "payment_bool": True,
            "stripe_checkout_id": "checkout_id_1"
        },
        {
            "user": user_instance,
            "product": product_instance,
            "payment_bool": False,
            "stripe_checkout_id": "checkout_id_2"
        },
    ]

    created_payment_infos = [repository.create(payment_info) for payment_info in payment_infos_data]
    retrieved_payment_infos = repository.get_all()

    assert len(retrieved_payment_infos) == 2
    assert set(retrieved_payment_infos) == set(created_payment_infos)


@pytest.mark.django_db
def test_get_by_id(repository, user_instance, product_instance):
    payment_info_data = {
        "user": user_instance,
        "product": product_instance,
        "payment_bool": True,
        "stripe_checkout_id": "some_checkout_id"
    }

    created_payment_info = repository.create(payment_info_data)
    retrieved_payment_info = repository.get_by_id(created_payment_info.id)

    assert retrieved_payment_info == created_payment_info


@pytest.mark.django_db
def test_get_by_id_not_found(repository):
    with pytest.raises(NotFound):
        repository.get_by_id(999)  # Assuming ID 999 doesn't exist


@pytest.mark.django_db
def test_update(repository, user_instance, product_instance):
    payment_info_data = {
        "user": user_instance,
        "product": product_instance,
        "payment_bool": True,
        "stripe_checkout_id": "some_checkout_id"
    }
    updated_data = {"payment_bool": False}

    created_payment_info = repository.create(payment_info_data)
    updated_payment_info = repository.update(created_payment_info.id, updated_data)

    assert updated_payment_info.payment_bool is False


@pytest.mark.django_db
def test_update_not_found(repository):
    with pytest.raises(NotFound):
        repository.update(999, {"payment_bool": False})  # Assuming ID 999 doesn't exist


@pytest.mark.django_db
def test_delete(repository, user_instance, product_instance):
    payment_info_data = {
        "user": user_instance,
        "product": product_instance,
        "payment_bool": True,
        "stripe_checkout_id": "some_checkout_id"
    }

    created_payment_info = repository.create(payment_info_data)
    repository.delete(created_payment_info.id)

    with pytest.raises(NotFound):
        repository.get_by_id(created_payment_info.id)
