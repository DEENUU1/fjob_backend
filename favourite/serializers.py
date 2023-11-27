from .models import Favourite
from rest_framework.serializers import ModelSerializer


class FavouriteSerializer(ModelSerializer):
    class Meta:
        model = Favourite
        fields = "__all__"
