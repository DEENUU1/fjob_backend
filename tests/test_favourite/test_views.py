import pytest
from rest_framework.test import force_authenticate, APIRequestFactory
from tests.fixtures import job_offer, user
from favourite.models import Favourite
from favourite.views import FavouriteCountAPIView

factory = APIRequestFactory()


@pytest.mark.django_db
def test_success_return_number_of_saved_to_favourites_for_specified_job_offer(job_offer, user):
    view = FavouriteCountAPIView.as_view()
    Favourite.objects.create(offer=job_offer, user=user)
    request = factory.get(f'/api/favourite/counter/{job_offer.id}')
    response = view(request, offer_id=job_offer.id)
    assert response.status_code == 200
    assert response.data['counter'] == 1
