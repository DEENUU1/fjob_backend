from .models import JobOffer
from django_filters import rest_framework as filters


class OffersFilter(filters.FilterSet):

    class Meta:
        model = JobOffer
        # JobOffer fields by which objects can be filtered
        fields = {
            "is_remote": ["exact"],
            "is_hybrid": ["exact"],
        }
