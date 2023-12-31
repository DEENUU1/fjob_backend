import json

import pytest
from rest_framework.test import force_authenticate, APIRequestFactory

from favourite.models import Favourite
from favourite.views import FavouriteView
from tests.fixtures import job_offer, user

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_return_list_of_favourite_job_offers_for_specified_user(user, job_offer):
    view = FavouriteView.as_view({"get": "list"})
    Favourite.objects.create(offer=job_offer, user=user)
    request = factory.get('/api/favourite/')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 200
    assert response.data[0]['id'] == job_offer.id


@pytest.mark.django_db
def test_error_list_of_favourite_job_offers_not_authenticated(user, job_offer):
    view = FavouriteView.as_view({"get": "list"})
    Favourite.objects.create(offer=job_offer, user=user)
    request = factory.get('/api/favourite/')
    response = view(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_success_create_favourite_job_offer_for_specified_user(user, job_offer):
    view = FavouriteView.as_view({"post": "create"})

    data = json.dumps({"offer_id": 1, "offer": 1, "user": user.id})

    request = factory.post('/api/favourite/', data, content_type='application/json')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 201


@pytest.mark.django_db
def test_error_create_favourite_job_offer_for_not_authenticated_user(user, job_offer):
    view = FavouriteView.as_view({"post": "create"})

    data = json.dumps({"offer_id": 1, "offer": 1, "user": user.id})

    request = factory.post('/api/favourite/', data, content_type='application/json')
    response = view(request)
    assert response.status_code == 401


@pytest.mark.django_db
def test_error_create_favourite_job_offer_already_saved(user, job_offer):
    view = FavouriteView.as_view({"post": "create"})
    Favourite.objects.create(offer=job_offer, user=user)
    data = json.dumps({"offer_id": 1, "offer": 1, "user": user.id})

    request = factory.post('/api/favourite/', data, content_type='application/json')
    force_authenticate(request, user=user)
    response = view(request)
    assert response.status_code == 400


@pytest.mark.django_db
def test_success_delete_favourite_job_offer_for_specified_user(user, job_offer):
    view = FavouriteView.as_view({"delete": "destroy"})
    favourite = Favourite.objects.create(offer=job_offer, user=user)

    request = factory.delete(f'/api/favourite/{favourite.id}/')
    force_authenticate(request, user=user)
    response = view(request, pk=favourite.id)
    assert response.status_code == 204


@pytest.mark.django_db
def test_error_delete_favourite_job_offer_for_not_authenticated_user(user, job_offer):
    view = FavouriteView.as_view({"delete": "destroy"})
    favourite = Favourite.objects.create(offer=job_offer, user=user)

    request = factory.delete(f'/api/favourite/{favourite.id}/')
    response = view(request, pk=favourite.id)
    assert response.status_code == 401
