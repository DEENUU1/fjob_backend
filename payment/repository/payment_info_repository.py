from ..models import PaymentInfo
from repository.crud import CRUDRepository


class PaymentInfoRepository(CRUDRepository):
    def __init__(self):
        super().__init__(PaymentInfo)
