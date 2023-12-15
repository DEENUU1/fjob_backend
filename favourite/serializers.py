from .models import Favourite
from rest_framework.serializers import ModelSerializer
from offer.models import JobOffer


class JobOfferSerializer(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ["id", "title"]


class FavouriteSerializer(ModelSerializer):
    offer = JobOfferSerializer()

    class Meta:
        model = Favourite
        fields = ["id", "user", "offer"]