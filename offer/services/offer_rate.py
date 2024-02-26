from collections import Counter

from django.shortcuts import get_object_or_404

from offer.models import JobOffer


class OfferRateService:
    """
    Service class for handling operations related to JobOfferRate entities.

    Methods:
    - __init__(self, repository): Constructor to initialize the service with a specified repository.
    - get_offer_rate_details(slug: str): Get details of the average rating and distribution of ratings for a JobOffer.

    Attributes:
    - _repository: The repository used for CRUD operations on JobOfferRate entities.
    """

    def __init__(self, repository):
        """
        Constructor to initialize the service with a specified repository.

        Parameters:
        - repository: The repository for CRUD operations on JobOfferRate entities.
        """
        self._repository = repository

    @staticmethod
    def get_offer_rate_details(slug: str):
        """
        Get details of the average rating and distribution of ratings for a JobOffer.

        Parameters:
        - slug: The unique identifier (slug) of the JobOffer.

        Returns:
        - result: Dictionary containing details of the average rating and distribution of ratings.
                  If no ratings are found, returns None.
        """
        job_offer = get_object_or_404(JobOffer, slug=slug)
        job_offer_rates = job_offer.jobofferrate_set.all()

        if not job_offer_rates:
            return None

        avg = sum(rate.rate for rate in job_offer_rates) / len(job_offer_rates)

        # Calculate JobOffer rates for 1, 2, 3, 4, 5 stars
        num_rates = len(job_offer_rates)
        rates = [rate.rate for rate in job_offer_rates]
        rates = Counter(rates)
        rates = [rates[1], rates[2], rates[3], rates[4], rates[5]]

        result = {
            "avg": avg,
            "num_rates": num_rates,
            "one_rate": rates[0],
            "two_rate": rates[1],
            "three_rate": rates[2],
            "four_rate": rates[3],
            "five_rate": rates[4],
        }
        return result
