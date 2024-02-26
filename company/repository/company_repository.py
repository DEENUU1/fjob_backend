from ..models import Company
from repository.crud import CRUDRepository


class CompanyRepository(CRUDRepository):
    def __init__(self):
        super().__init__(Company)
