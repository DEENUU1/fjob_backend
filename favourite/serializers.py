from rest_framework.serializers import ModelSerializer, ValidationError

from offer.serializers import JobOfferHelperSerializer
from .models import Favourite


class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = ("id", "user", "offer",)

    def validate(self, data):
        user = self.context['request'].user
        offer = data['offer']

        # Check if Favourite object already exists for the current user and offer
        existing_favourite = Favourite.objects.filter(
            user=user,
            offer=offer,
        ).first()

        if existing_favourite:
            raise ValidationError("Job Offer is already saved to Favourite")

        return data


class FavouriteSerializerList(ModelSerializer):
    offer = JobOfferHelperSerializer()

    class Meta:
        model = Favourite
        fields = ("id", "user", "offer",)
