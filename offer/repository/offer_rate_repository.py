from ..models import JobOfferRate
from repository.crud import CRUDRepository


class JobOfferRateRepository(CRUDRepository):
    """
    Repository class for CRUD operations on JobOfferRate model.

    Inherits from CRUDRepository.

    Methods:
    - __init__(self): Constructor to initialize the repository with the JobOfferRate model.

    Attributes:
    - None
    """

    def __init__(self):
        """
        Constructor to initialize the repository with the JobOfferRate model.
        """
        super().__init__(JobOfferRate)
