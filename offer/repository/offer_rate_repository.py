from ..models import JobOfferRate
from repository.crud import CRUDRepository


class JobOfferRateRepository(CRUDRepository):
    def __init__(self):
        super().__init__(JobOfferRate)
