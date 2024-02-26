class OfferService:
    """
    Service class for handling operations related to JobOffer entities.

    Methods:
    - __init__(self, repository): Constructor to initialize the service with a specified repository.
    - save_scraped_offers(self, data): Save scraped job offers into the repository.

    Attributes:
    - _repository: The repository used for CRUD operations on JobOffer entities.
    """

    def __init__(self, repository):
        """
        Constructor to initialize the service with a specified repository.

        Parameters:
        - repository: The repository for CRUD operations on JobOffer entities.
        """
        self._repository = repository

    def save_scraped_offers(self, data):
        """
        Save scraped job offers into the repository.

        Parameters:
        - data: List of dictionaries containing scraped job offer data.
        """
        for item in data:
            self._repository.save_scraped(item)
