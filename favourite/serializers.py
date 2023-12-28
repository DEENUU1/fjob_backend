from rest_framework.serializers import ModelSerializer

from offer.models import JobOffer
from .models import Favourite


class JobOfferSerializer(ModelSerializer):
    class Meta:
        model = JobOffer
        fields = ("id", "title",)


class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("id", "user", "offer",)


class FavouriteSerializerList(ModelSerializer):
    offer = JobOfferSerializer()

    class Meta:
        model = Favourite
        fields = ("id", "user", "offer",)
