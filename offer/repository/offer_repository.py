from ..models import JobOffer
from repository.crud import CRUDRepository


class OfferRepository(CRUDRepository):
    def __init__(self):
        super().__init__(JobOffer)
